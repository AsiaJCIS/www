/* Shared navigation bar for AsiaJCIS 2026 */
(function () {
  const navHTML = `
  <nav class="navbar navbar-expand-lg fixed-top shadow-sm" id="mainNav">
    <div class="container-xl">
      <a class="navbar-brand text-white fw-bold" href="index.html">
        <span style="color:#e8622a;">Asia</span>JCIS <span class="text-white-50 fw-normal">2026</span>
      </a>
      <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link" href="index.html">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="callforpapers.html">Call for Papers</a>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">Program</a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="program.html"><i class="bi bi-calendar3 me-2"></i>Conference Program</a></li>
              <li><a class="dropdown-item" href="acceptedpaper.html"><i class="bi bi-journal-check me-2"></i>Accepted Papers</a></li>
              <li><a class="dropdown-item" href="proceedings.html"><i class="bi bi-book me-2"></i>Proceedings</a></li>
            </ul>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="submission.html">Submission</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="committee.html">Committees</a>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">Registration</a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><a class="dropdown-item" href="registration.html"><i class="bi bi-pencil-square me-2"></i>Registration</a></li>
              <li><a class="dropdown-item" href="venue.html"><i class="bi bi-geo-alt me-2"></i>Venue Info</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>`;

  // Insert at top of body
  document.body.insertAdjacentHTML('afterbegin', navHTML);

  // Highlight active page
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('#mainNav .nav-link, #mainNav .dropdown-item').forEach(el => {
    if (el.getAttribute('href') === path) {
      el.classList.add('active');
      // Also mark parent dropdown toggle
      const dropParent = el.closest('.dropdown');
      if (dropParent) dropParent.querySelector('.dropdown-toggle').classList.add('active');
    }
  });
})();
