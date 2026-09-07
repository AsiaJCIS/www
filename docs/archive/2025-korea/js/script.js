document.addEventListener('DOMContentLoaded', function () {
    // 요소 선택
    const hamburger = document.querySelector('.hamburger');
    const nav = document.querySelector('nav');
    const body = document.body;

    // 오버레이 요소 생성
    const overlay = document.createElement('div');
    overlay.className = 'overlay';
    body.appendChild(overlay);

    // 햄버거 메뉴 클릭 이벤트
    hamburger.addEventListener('click', function () {
        nav.classList.toggle('active');
        overlay.classList.toggle('active');
        body.classList.toggle('no-scroll'); // 메뉴 열릴 때 스크롤 방지 (선택사항)
    });

    // 오버레이 클릭 시 메뉴 닫기
    overlay.addEventListener('click', function () {
        nav.classList.remove('active');
        overlay.classList.remove('active');
        body.classList.remove('no-scroll');
    });

    // 서브메뉴를 가진 항목 처리
    const menuItems = document.querySelectorAll('nav > ul > li');

    menuItems.forEach(item => {
        if (item.querySelector('ul')) {
            item.classList.add('has-submenu');

            // 서브메뉴 토글 이벤트
            item.querySelector('a').addEventListener('click', function (e) {
                // 모바일 환경에서만 작동
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    item.classList.toggle('submenu-active');

                    // 다른 열린 서브메뉴 닫기 (선택사항)
                    menuItems.forEach(otherItem => {
                        if (otherItem !== item && otherItem.classList.contains('submenu-active')) {
                            otherItem.classList.remove('submenu-active');
                        }
                    });
                }
            });
        }
    });

    // 화면 크기 변경 시 초기화
    window.addEventListener('resize', function () {
        if (window.innerWidth > 768) {
            nav.classList.remove('active');
            overlay.classList.remove('active');
            body.classList.remove('no-scroll');

            menuItems.forEach(item => {
                item.classList.remove('submenu-active');
            });
        }
    });
});