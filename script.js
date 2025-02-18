document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM полностью загружен и разобран');
    document.getElementById('downloadBtn').addEventListener('click', function() {
        const installationFile = '../Setup.exe';
        
        // Создаем ссылку для загрузки
        const link = document.createElement('a');
        link.href = installationFile;
        link.download = 'Setup.exe'; // Имя файла при загрузке
        
        // Добавляем ссылку на страницу, кликаем по ней и удаляем
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.location.href = '../thanks.html';
    });


    // Анимация появления секций при прокрутке
    const sections = document.querySelectorAll('section');
    
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };
    
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    sections.forEach(section => {
        observer.observe(section);
    });
  // Сюда чисто свой код, там вставлять html через json, чтобы с бэка приходили данные и ты их из json брал, удобно короче и страница будет норм прогружаться, то есть html добавится после того, как док будет загружен и не будет ошибок в изображении страницы
});


