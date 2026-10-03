function toggleMenu() {
    document.querySelector('.nav').classList.toggle('mobile-ouvert');
}

document.querySelectorAll('.nav a').forEach(link => {
    link.addEventListener('click', () => {
        document.querySelector('.nav').classList.remove('mobile-ouvert');
    });
});

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

function animerChiffre(element) {
    const texte = element.textContent;
    const match = texte.match(/[\d.]+/);
    if (!match) return;
    const nombreFinal = parseFloat(match[0]);
    const prefixe = texte.substring(0, match.index);
    const suffixe = texte.substring(match.index + match[0].length);
    const debut = performance.now();
    function update(now) {
        const progression = Math.min((now - debut) / 1500, 1);
        const valeur = Math.floor(nombreFinal * (1 - Math.pow(1 - progression, 3)));
        element.textContent = prefixe + valeur + suffixe;
        if (progression < 1) requestAnimationFrame(update);
        else element.textContent = texte;
    }
    requestAnimationFrame(update);
}

document.querySelectorAll('.chiffre-valeur').forEach(el => {
    const obs = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animerChiffre(entry.target);
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    obs.observe(el);
});

console.log("🚀 Site ETI v2.0 chargé");