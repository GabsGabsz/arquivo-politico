const menuButton=document.querySelector('.menu-button');
const menu=document.querySelector('.navlinks');
menuButton?.addEventListener('click',()=>{const opened=menu.classList.toggle('open');menuButton.setAttribute('aria-expanded',String(opened));menuButton.textContent=opened?'Fechar ×':'Menu +';});
menu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.classList.remove('open');menuButton.setAttribute('aria-expanded','false');menuButton.textContent='Menu +';}));
const search=document.getElementById('candidate-search');
const grid=document.querySelector('.candidates-grid');
if(search && grid){
 const cards=[...grid.querySelectorAll('.candidate-card')];
 const normalized=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
 search.addEventListener('input',()=>{
  const query=normalized(search.value);
  let count=0;
  cards.forEach(card=>{const match=normalized(card.dataset.search).includes(query);card.hidden=!match;if(match)count++;});
  document.getElementById('candidate-count').textContent=`${count} ${count===1?'candidato encontrado':'candidatos encontrados'}`;
  grid.querySelector('.no-results').hidden=count>0;
 });
}
