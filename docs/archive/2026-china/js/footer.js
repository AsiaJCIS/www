/* Shared footer for AsiaJCIS 2026 */
(function () {
  const footerHTML = `
  <footer class="mt-5">
    <div class="container-xl">
      <div class="row gy-4">
        <div class="col-md-4">
          <h6 class="text-white fw-bold mb-3"><span style="color:#e8622a;">Asia</span>JCIS 2026</h6>
          <p class="mb-1" style="font-size:.85rem;">21st Asia Joint Conference on<br>Information Security</p>
          <p class="mb-0" style="font-size:.85rem;"><i class="bi bi-calendar3 me-1"></i>August 4–5, 2026</p>
          <p style="font-size:.85rem;"><i class="bi bi-geo-alt me-1"></i>Guangdong, China</p>
        </div>
        <div class="col-md-4">
          <h6 class="text-white fw-bold mb-3">Quick Links</h6>
          <ul class="list-unstyled" style="font-size:.85rem;">
            <li><a href="callforpapers.html">Call for Papers</a></li>
            <li><a href="program.html">Conference Program</a></li>
            <li><a href="registration.html">Registration</a></li>
            <li><a href="venue.html">Venue Info</a></li>
            <li><a href="committee.html">Committees</a></li>
          </ul>
        </div>
        <div class="col-md-4">
          <h6 class="text-white fw-bold mb-3">Contact</h6>
          <p style="font-size:.85rem;"><i class="bi bi-envelope me-1"></i><a href="mailto:asiajcis2026@easychair.org">asiajcis2026@easychair.org</a></p>
          <p style="font-size:.85rem;"><i class="bi bi-envelope me-1"></i><a href="mailto:changsongyang@guet.edu.cn">changsongyang@guet.edu.cn</a></p>
        </div>
      </div>
      <hr class="footer-divider my-3">
      <p class="text-center mb-0" style="font-size:.82rem;">&copy; 2026 AsiaJCIS Conference. All rights reserved. | Hosted by Guangdong University of Science and Technology</p>
    </div>
  </footer>`;

  document.body.insertAdjacentHTML('beforeend', footerHTML);
})();
