#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sijut2.py — Cliente de consulta e raspagem do SIJUT2 (Sistema de Informações
sobre a Jurisprudência e a legislação Tributária da Receita Federal do Brasil).

Base pública: https://normas.receita.fazenda.gov.br/sijut2consulta/

O SIJUT2 NÃO expõe uma API JSON oficial: é uma aplicação Struts2 que renderiza
HTML no servidor. Este script encapsula os dois endpoints úteis:

  * consulta.action  -> formulário/resultado da busca (lista de atos)
  * link.action      -> texto integral de um ato, via ?idAto=<id>&visao=<visao>

Uso rápido:

    # Lista os códigos de "tipo de ato" (tiposAtosSelecionados) direto do form
    python3 sijut2.py tipos

    # Apenas monta a URL de busca (funciona OFFLINE — útil para colar no navegador)
    python3 sijut2.py url --tipo 59 --termo '"crédito presumido"' --ano 2024

    # Busca Pareceres Normativos (tipo 59) contendo um termo
    python3 sijut2.py buscar --tipo 59 --termo '"ágio"' --ano 2023

    # Texto integral de um ato (visão compilada = texto consolidado atual)
    python3 sijut2.py texto --id 123456 --visao compilado

Operadores de busca aceitos pelo termoBusca (parâmetro `termo`):
    "frase exata"      -> aspas para expressão literal
    palavra1 AND palavra2   -> exige ambas
    palavra1 NOT palavra2   -> exclui a segunda

Rede: em ambientes com proxy corporativo (ex.: Claude Code), este script
respeita HTTPS_PROXY e o bundle de CA em REQUESTS_CA_BUNDLE / SSL_CERT_FILE.
Se o domínio da Receita estiver bloqueado pela política de egresso, a chamada
retorna 403/erro de túnel — isso é política de rede, não bug do script; rode a
partir de um ambiente com acesso liberado ao domínio da Receita.
"""

import argparse
import html
import os
import re
import sys
import textwrap
import urllib.parse

try:
    import requests
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "Falta a biblioteca 'requests'. Instale com: pip install requests\n"
    )
    raise

BASE = "https://normas.receita.fazenda.gov.br/sijut2consulta/"
CONSULTA = BASE + "consulta.action"
LINK = BASE + "link.action"

# User-Agent identificável e educado. Ajuste o contato se for uso institucional.
UA = "consulta-normas-tributarias/1.0 (uso profissional; respeita robots)"

# Ordem dos parâmetros seguindo o formulário original do SIJUT2.
DEFAULT_PARAMS = {
    "facetsExistentes": "",
    "orgaosSelecionados": "",
    "tiposAtosSelecionados": "",
    "lblTiposAtosSelecionados": "",
    "tipoAtoFacet": "",
    "siglaOrgaoFacet": "",
    "anoAtoFacet": "",
    "termoBusca": "",
    "numero_ato": "",
    "tipoData": "2",
    "dt_inicio": "",
    "dt_fim": "",
    "ano_ato": "",
    "p": "1",  # página de resultados
}


def _session():
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9"})
    # requests já lê REQUESTS_CA_BUNDLE/CURL_CA_BUNDLE; reforçamos SSL_CERT_FILE.
    ca = os.environ.get("REQUESTS_CA_BUNDLE") or os.environ.get("SSL_CERT_FILE")
    if ca and os.path.exists(ca):
        s.verify = ca
    return s


def build_url(termo="", tipo="", numero="", ano="", dt_inicio="", dt_fim="",
              pagina=1, extra=None):
    """Monta a URL de consulta.action. Puro — não faz rede."""
    p = dict(DEFAULT_PARAMS)
    p["termoBusca"] = termo or ""
    p["tiposAtosSelecionados"] = str(tipo) if tipo else ""
    p["numero_ato"] = str(numero) if numero else ""
    p["ano_ato"] = str(ano) if ano else ""
    p["anoAtoFacet"] = str(ano) if ano else ""
    p["dt_inicio"] = dt_inicio or ""
    p["dt_fim"] = dt_fim or ""
    p["p"] = str(pagina)
    if extra:
        p.update(extra)
    return CONSULTA + "?" + urllib.parse.urlencode(p)


def _get(session, url):
    resp = session.get(url, timeout=40)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or "utf-8"
    return resp.text


TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"[ \t]+")


def _strip(fragment):
    txt = html.unescape(TAG_RE.sub(" ", fragment))
    txt = WS_RE.sub(" ", txt)
    return re.sub(r"\n\s*\n\s*\n+", "\n\n", txt).strip()


def parse_resultados(html_text):
    """
    Extrai os atos de uma página de resultado.

    A estrutura do SIJUT2 é HTML renderizado no servidor e pode mudar. A âncora
    para o texto do ato — link.action?idAto=NNN — é o ponto estável: capturamos
    cada idAto e o texto visível da âncora (título/ementa do ato). Se o layout
    mudar e a extração ficar vazia, use --raw para inspecionar o HTML e ajustar.
    """
    resultados = []
    vistos = set()
    # <a ... href="...link.action?idAto=123&...">TÍTULO / EMENTA</a>
    for m in re.finditer(
        r'href="([^"]*link\.action\?[^"]*idAto=(\d+)[^"]*)"[^>]*>(.*?)</a>',
        html_text,
        re.IGNORECASE | re.DOTALL,
    ):
        href, id_ato, anchor = m.group(1), m.group(2), _strip(m.group(3))
        if id_ato in vistos:
            continue
        vistos.add(id_ato)
        if href.startswith("/"):
            href = "https://normas.receita.fazenda.gov.br" + href
        elif not href.startswith("http"):
            href = BASE + href.lstrip("./")
        resultados.append({"idAto": id_ato, "titulo": anchor, "url": href})
    return resultados


def parse_tipos(html_text):
    """Extrai o mapa de tipos de ato do <select> do formulário de consulta."""
    tipos = []
    # tenta isolar o select de tipos; se falhar, varre todos os <option> numéricos
    bloco = re.search(
        r'<select[^>]*(?:tiposAtos|tipoAto)[^>]*>(.*?)</select>',
        html_text, re.IGNORECASE | re.DOTALL,
    )
    escopo = bloco.group(1) if bloco else html_text
    for m in re.finditer(r'<option[^>]*value="(\d+)"[^>]*>(.*?)</option>',
                         escopo, re.IGNORECASE | re.DOTALL):
        code, label = m.group(1), _strip(m.group(2))
        if label:
            tipos.append((code, label))
    # dedup preservando ordem
    seen, out = set(), []
    for c, l in tipos:
        if c not in seen:
            seen.add(c)
            out.append((c, l))
    return out


def cmd_url(args):
    print(build_url(termo=args.termo or "", tipo=args.tipo or "",
                    numero=args.numero or "", ano=args.ano or "",
                    dt_inicio=args.dt_inicio or "", dt_fim=args.dt_fim or "",
                    pagina=args.pagina))


def cmd_tipos(args):
    s = _session()
    html_text = _get(s, CONSULTA)
    tipos = parse_tipos(html_text)
    if not tipos:
        sys.stderr.write("Nenhum tipo extraído — layout pode ter mudado. "
                         "Rode 'buscar --raw' para inspecionar o HTML.\n")
        return 2
    for code, label in tipos:
        print(f"{code}\t{label}")
    return 0


def cmd_buscar(args):
    s = _session()
    url = build_url(termo=args.termo or "", tipo=args.tipo or "",
                    numero=args.numero or "", ano=args.ano or "",
                    dt_inicio=args.dt_inicio or "", dt_fim=args.dt_fim or "",
                    pagina=args.pagina)
    sys.stderr.write(f"[GET] {url}\n")
    html_text = _get(s, url)
    if args.raw:
        sys.stdout.write(html_text)
        return 0
    resultados = parse_resultados(html_text)
    if not resultados:
        sys.stderr.write(
            "Zero atos extraídos. Ou a busca não retornou nada, ou o layout "
            "mudou. Confira no navegador com: python3 sijut2.py url ...  ou "
            "reveja o HTML com --raw.\n"
        )
        return 1
    for r in resultados:
        print(f"idAto={r['idAto']}\t{r['titulo']}")
        print(f"    {r['url']}")
    sys.stderr.write(f"\n{len(resultados)} ato(s) nesta página "
                     f"(use --pagina N para as próximas).\n")
    return 0


def cmd_texto(args):
    s = _session()
    params = {"idAto": str(args.id), "visao": args.visao}
    url = LINK + "?" + urllib.parse.urlencode(params)
    sys.stderr.write(f"[GET] {url}\n")
    html_text = _get(s, url)
    if args.raw:
        sys.stdout.write(html_text)
        return 0
    print(_strip(html_text))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="sijut2.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(__doc__),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--termo", help="termoBusca (aceita aspas, AND, NOT)")
    common.add_argument("--tipo", help="código do tipo de ato "
                        "(veja 'tipos'; 59 = Parecer Normativo/PN)")
    common.add_argument("--numero", help="número do ato")
    common.add_argument("--ano", help="ano do ato")
    common.add_argument("--dt-inicio", dest="dt_inicio", help="dd/mm/aaaa")
    common.add_argument("--dt-fim", dest="dt_fim", help="dd/mm/aaaa")
    common.add_argument("--pagina", type=int, default=1, help="página (default 1)")

    b = sub.add_parser("buscar", parents=[common], help="busca atos e lista idAto/título")
    b.add_argument("--raw", action="store_true", help="imprime o HTML bruto")
    b.set_defaults(func=cmd_buscar)

    u = sub.add_parser("url", parents=[common], help="só monta a URL (offline)")
    u.set_defaults(func=cmd_url)

    t = sub.add_parser("tipos", help="lista códigos de tipo de ato do formulário")
    t.set_defaults(func=cmd_tipos)

    x = sub.add_parser("texto", help="texto integral de um ato por idAto")
    x.add_argument("--id", required=True, help="idAto")
    x.add_argument("--visao", default="compilado",
                   choices=["compilado", "anotado", "original"],
                   help="compilado=texto consolidado atual; "
                        "anotado=com marcações de alteração; original=redação original")
    x.add_argument("--raw", action="store_true", help="imprime o HTML bruto")
    x.set_defaults(func=cmd_texto)

    args = p.parse_args(argv)
    try:
        return args.func(args) or 0
    except requests.exceptions.SSLError as e:
        sys.stderr.write(f"Erro de TLS: {e}\nAponte REQUESTS_CA_BUNDLE para o "
                         "bundle de CA do proxy.\n")
        return 3
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code if e.response is not None else "?"
        sys.stderr.write(f"HTTP {code} ao acessar a Receita. Se for 403/407, o "
                         "domínio pode estar bloqueado pela política de rede do "
                         "ambiente — rode de onde o acesso é liberado.\n")
        return 4
    except requests.exceptions.RequestException as e:
        sys.stderr.write(f"Falha de rede: {e}\n")
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
