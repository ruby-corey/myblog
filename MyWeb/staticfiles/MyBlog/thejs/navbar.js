/* 添加JavaScript滚动监听 */

document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.transparent-navbar');
    
    window.addEventListener('scroll', function() {
        // 当滚动超过50px时添加scrolled类
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
});

/* 更换主题 */
// 主题切换功能
document.addEventListener('DOMContentLoaded', function() {
    const themeSwitcher = document.getElementById('themeSwitcher');
    const htmlElement = document.documentElement;
    
    // 检查本地存储中的主题设置
    const savedTheme = localStorage.getItem('theme');
    
    // 设置初始主题
    if (savedTheme) {
        htmlElement.setAttribute('data-theme', savedTheme);
    } else {
        // 默认跟随系统偏好
        const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
        if (prefersDarkScheme.matches) {
            htmlElement.setAttribute('data-theme', 'dark');
        }
    }
    
    // 切换主题
    themeSwitcher.addEventListener('click', function() {
        const currentTheme = htmlElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        htmlElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        

    });
    

});