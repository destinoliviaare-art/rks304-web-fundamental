(function () {
  // =========================================================
  // Interaksi ringan: underline nav berjalan, efek "decrypt"
  // pada nama di hero, tilt kartu proyek, scroll reveal,
  // dan validasi form contact.
  // Setiap fungsi otomatis "no-op" kalau elemen terkait
  // tidak ada di halaman yang sedang dibuka.
  // =========================================================

  document.addEventListener('DOMContentLoaded', () => {
    initNavIndicator();
    initDecryptName();
    initCardTilt();
    initContactForm();
    initScrollReveal();
  });

  /* ---------- 1. Kotak bertepi tumpul yang meluncur ke tautan aktif / di-hover ---------- */
  function initNavIndicator() {
    const nav = document.querySelector('.main-nav ul');
    const indicator = document.querySelector('.nav-indicator');
    const links = document.querySelectorAll('.main-nav a');
    const activeLink = document.querySelector('.main-nav a[aria-current="page"]');
    if (!nav || !indicator || !links.length) return;

    const moveTo = (el) => {
      if (!el) return;
      const navRect = nav.getBoundingClientRect();
      const rect = el.getBoundingClientRect();
      indicator.style.left = (rect.left - navRect.left) + 'px';
      indicator.style.top = (rect.top - navRect.top) + 'px';
      indicator.style.width = rect.width + 'px';
      indicator.style.height = rect.height + 'px';
      indicator.classList.add('is-visible');
    };

    moveTo(activeLink);

    links.forEach(link => {
      link.addEventListener('mouseenter', () => moveTo(link));
    });

    nav.addEventListener('mouseleave', () => moveTo(activeLink));

    window.addEventListener('resize', () => {
      moveTo(document.querySelector('.main-nav a:hover') || activeLink);
    });
  }

  /* ---------- 2. Nama di hero "terdekripsi" sekali saat halaman dibuka ---------- */
  function initDecryptName() {
    const el = document.querySelector('.decrypt-name');
    if (!el) return;

    const finalText = el.textContent;
    const glyphs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ#%&$*/<>01';
    const chars = finalText.split('').map(ch => {
      const span = document.createElement('span');
      span.className = 'char';
      span.textContent = ch === ' ' ? '\u00A0' : ch;
      return { span, target: ch };
    });

    el.textContent = '';
    chars.forEach(c => el.appendChild(c.span));

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      return; // biarkan teks final tampil apa adanya
    }

    const revealDelayPerChar = 45;
    const scrambleTicks = 6;
    const tickInterval = 28;

    chars.forEach((c, i) => {
      if (c.target === ' ') return;
      let tick = 0;
      const startAt = i * revealDelayPerChar;
      setTimeout(() => {
        const scrambleTimer = setInterval(() => {
          c.span.textContent = glyphs[Math.floor(Math.random() * glyphs.length)];
          tick++;
          if (tick >= scrambleTicks) {
            clearInterval(scrambleTimer);
            c.span.textContent = c.target;
          }
        }, tickInterval);
      }, startAt);
    });
  }

  /* ---------- 3. Efek tilt halus saat kursor di atas kartu proyek ---------- */
  function initCardTilt() {
    const cards = document.querySelectorAll('.card');
    if (!cards.length) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (window.matchMedia('(hover: none)').matches) return; // skip di touch device

    const maxTilt = 6; // derajat

    cards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width;  // 0..1
        const y = (e.clientY - rect.top) / rect.height;  // 0..1
        const rotateY = (x - 0.5) * (maxTilt * 2);
        const rotateX = (0.5 - y) * (maxTilt * 2);
        card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg)';
      });
    });
  }

  /* ---------- 4. Section & kartu muncul halus saat masuk viewport ---------- */
  function initScrollReveal() {
    const targets = document.querySelectorAll('.section, .card, .page-intro');
    if (!targets.length) return;

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) {
      targets.forEach(el => el.classList.add('is-visible'));
      return;
    }

    targets.forEach(el => el.classList.add('reveal'));

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    targets.forEach(el => observer.observe(el));
  }

  /* ---------- 5. Form contact: validasi bawaan + status pesan ---------- */
  function initContactForm() {
    const form = document.getElementById('contact-form');
    const status = document.getElementById('form-status');
    if (!form || !status) return;

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      status.textContent = 'Terima kasih! Pesanmu sudah "terkirim" (form demo, belum tersambung ke server).';
      form.reset();
    });
  }
})();
