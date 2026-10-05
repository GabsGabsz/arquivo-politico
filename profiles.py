"""Render sourced candidate profiles and election cards as accessible static HTML."""
import json
import math
from html import escape

def esc(value):
    return escape(str(value), quote=True)

def photo_credit(photo):
    credit = f'<a href="{esc(photo["url"])}" target="_blank" rel="noopener noreferrer">Foto: {esc(photo["credit"])} ↗</a>'
    if photo.get('license'):
        credit += f' · <a href="{esc(photo["licenseUrl"])}" target="_blank" rel="noopener noreferrer">{esc(photo["license"])}</a>'
    return f'<figcaption class="photo-credit">{credit}<span>{esc(photo["year"])}</span></figcaption>'

def candidate_cards(root):
    metadata = json.loads((root/'content/candidates.json').read_text())
    cards = []
    for c in metadata['candidates']:
        photo = metadata['photoCredits'][c['id']]
        url = '/candidatos/'+c['id']+'/'
        src = photo.get('src', '/assets/'+c['id']+'.jpg')
        cards.append(f'''<article class="candidate-card" data-search="{esc(c['name']+' '+c['short']+' '+c['party'])}"><a class="candidate-cover has-photo" href="{url}" aria-label="Conhecer a trajetória de {esc(c['short'])}"><img class="candidate-photo photo-{c['id']}" src="{esc(src)}" referrerpolicy="no-referrer" alt="Retrato de {esc(c['short'])}" width="354" height="472" loading="lazy" decoding="async"><span class="cover-meta"><span>{c['party']} / 2002</span><span>BR ↗</span></span><span><span class="ballot">{c['number']}</span><span class="ballot-label">NÚMERO NA URNA</span></span><span class="open-icon" aria-hidden="true">↗</span></a><div class="photo-credit"><a href="{esc(photo['url'])}" target="_blank" rel="noopener noreferrer">Foto: {esc(photo['credit'])} ↗</a>{(' · <a href="'+esc(photo['licenseUrl'])+'" target="_blank" rel="noopener noreferrer">'+esc(photo['license'])+'</a>') if photo.get('license') else ''}</div><h3><a href="{url}">{esc(c['short'])}</a></h3><p>{esc(c['desc'])}</p><a class="card-link" href="{url}">Explorar trajetória ↗</a></article>''')
    return ''.join(cards)+'<p class="no-results" hidden>Nenhum candidato encontrado. Tente outro nome ou partido.</p>'

def render_profiles(root, head, footer, output_dir=None):
    data = json.loads((root/'content/profiles.json').read_text())
    metadata = json.loads((root/'content/candidates.json').read_text())
    candidates = {c['id']:c for c in metadata['candidates']}
    for index, profile in enumerate(data):
        cid = profile['id']
        c = candidates[cid]
        photo = metadata['photoCredits'][cid]
        numbers = {source['id']:i+1 for i,source in enumerate(profile['sources'])}
        def refs(ids):
            return ' <span class="inline-refs">'+''.join(f'<a class="source-ref" href="#fonte-{esc(sid)}" aria-label="Consultar fonte {numbers[sid]}">[{numbers[sid]}]</a>' for sid in ids)+'</span>' if ids else ''
        minutes = max(1, math.ceil(len(' '.join(p['text'] for s in profile['sections'] for p in s['paragraphs']).split())/200)+2)
        src = photo.get('src','/assets/'+cid+'.jpg')
        page = head(esc(c['short'])+' — trajetória política',esc(profile['summary']))
        page += f'''<div class="wrap breadcrumb"><a href="/">Início</a><span>/</span><a href="/eleicoes/2002/#candidatos">Eleição 2002</a><span>/</span><span aria-current="page">{esc(c['short'])}</span></div><section class="wrap profile-hero"><div><div class="eyebrow">Arquivo de trajetórias / Eleição 2002</div><h1>{esc(c['short'])}<span class="profile-cursor" aria-hidden="true">_</span></h1><p class="profile-subtitle">{esc(profile['subtitle'])}</p><p class="profile-summary">{esc(profile['summary'])}</p><div class="profile-facts"><div><span>NOME COMPLETO</span><strong>{esc(c['name'])}</strong></div><div><span>NA URNA EM 2002</span><strong>{c['party']} · {c['number']}</strong></div></div><div class="profile-edition mono">LEITURA: ~{minutes} MIN · REVISÃO: 05 OUT 2026</div></div><figure class="profile-portrait"><div><img src="{esc(src)}" alt="Retrato de {esc(c['short'])}" width="354" height="472" referrerpolicy="no-referrer" fetchpriority="high"><span class="portrait-label">ARQUIVO / {c['number']}</span></div>{photo_credit(photo)}</figure></section><div class="wrap profile-method"><span class="mono">COMO LER</span><p>O partido no cabeçalho é o da eleição de 2002. As referências numeradas levam às fontes de cada trecho. Proposta, execução e resultado são tratados separadamente; processos são descritos conforme as decisões e datas documentadas.</p></div><div class="wrap profile-layout"><aside class="profile-sidebar"><nav aria-label="Nesta trajetória"><span class="eyebrow">Nesta trajetória</span><a href="#linha-do-tempo">Linha do tempo</a>'''
        page += ''.join(f'<a href="#{esc(s["id"])}">{esc(s["title"])}</a>' for s in profile['sections'])
        page += '<a href="#propostas">Propostas e prática</a><a href="#limites">Alcance da pesquisa</a><a href="#fontes">Fontes consultadas</a></nav><a class="profile-back" href="/eleicoes/2002/#candidatos">← Os seis candidatos</a></aside><div class="profile-reading"><section class="profile-section" id="linha-do-tempo"><div class="eyebrow">A trajetória em perspectiva</div><h2>Uma vida, vários capítulos.</h2><ol class="profile-timeline">'
        for event in profile['timeline']:
            page += f'<li><span class="timeline-date">{esc(event["date"])}</span><h3>{esc(event["title"])}</h3><p>{esc(event["text"])}{refs(event["sources"])}</p></li>'
        page += '</ol></section>'
        for n, section in enumerate(profile['sections'],1):
            page += f'<section class="profile-section" id="{esc(section["id"])}"><div class="eyebrow">{n:02d} / A história por trás do voto</div><h2>{esc(section["title"])}</h2>'
            page += ''.join(f'<p>{esc(p["text"])}{refs(p["sources"])}</p>' for p in section['paragraphs'])
            page += '</section>'
        page += '<section class="profile-section" id="propostas"><div class="eyebrow">Do discurso à atuação</div><h2>Propostas e prática.</h2><p class="section-intro">Uma seleção de compromissos e políticas documentados. O cargo, o período e a responsabilidade por cada resultado fazem parte da avaliação.</p><div class="commitments">'
        for item in profile['commitments']:
            page += f'<article class="commitment"><span class="commitment-status">{esc(item["status"])}</span><h3>{esc(item["promise"])}</h3><div class="commitment-detail"><span>O QUE ACONTECEU</span><p>{esc(item["outcome"])}</p></div><div class="commitment-detail"><span>CONTEXTO PARA AVALIAR</span><p>{esc(item["context"])}{refs(item["sources"])}</p></div></article>'
        page += '</div></section><section class="profile-section research-limits" id="limites"><div class="eyebrow">Transparência editorial</div><h2>O alcance desta pesquisa.</h2><ul>'+''.join(f'<li>{esc(limit)}</li>' for limit in profile['limits'])+'</ul><p>Esta página não é uma certidão judicial nem um inventário de todos os atos da carreira. Uma decisão processual, uma absolvição e uma condenação têm significados distintos. Não atribuímos nota geral ou recomendação de voto.</p></section><section class="profile-section profile-sources" id="fontes"><div class="eyebrow">Verifique por conta própria</div><h2>Fontes consultadas.</h2><p>Documentos públicos, registros eleitorais, pesquisas, imprensa e materiais dos próprios candidatos ou partidos, identificados abaixo.</p><ol>'
        for s in profile['sources']:
            page += f'<li id="fonte-{esc(s["id"])}"><a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["title"])} ↗</a><span>{esc(s["publisher"])}'+(f' · {esc(s["date"])}' if s.get('date') else '')+'</span></li>'
        page += '</ol></section></div></div>'
        others = [v for v in metadata['candidates'] if v['id'] != cid]
        page += '<section class="profile-others"><div class="wrap"><div class="eyebrow">Continue no arquivo de 2002</div><h2>Outras trajetórias, a mesma eleição.</h2><div>'+''.join(f'<a href="/candidatos/{o["id"]}/"><span>{esc(o["short"])}</span><span class="mono">{o["party"]} ↗</span></a>' for o in others)+'</div><a class="backlink" href="/eleicoes/2002/#candidatos">← Voltar à eleição de 2002</a></div></section>'+footer
        target = (output_dir if output_dir is not None else root/'dist')/'candidatos'/cid
        target.mkdir(parents=True,exist_ok=True)
        (target/'index.html').write_text(page)
    print(f'Generated {len(data)} sourced candidate profiles.')
