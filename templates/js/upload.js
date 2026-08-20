document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('dropzone');
    const fileUpload = document.getElementById('file-upload');
    const currentUploadInput = document.querySelector('.upload__input');

    <!-- TODO !!!!!!!!!!!!!!!!!!!!!!!! ДОБАВИТЬ РАСШИРЕНИЯ -->
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    const MAX_SIZE_MB = 5;
    const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;

    // Клик по зоне открывает системный диалог выбора файла
    dropzone.addEventListener('click', () => {
        fileUpload.click();
    });

    const validateFile = (file) => {
        if (!allowedTypes.includes(file.type)) {
            alert('Неверный формат файла. Разрешены: .jpg, .jpeg, .png, .gif');
            return false;
        }
        if (file.size > MAX_SIZE_BYTES) {
            alert(`Файл слишком большой. Максимум — ${MAX_SIZE_MB} МБ`);
            return false;
        }
        return true;
    };

    const uploadFile = async (file) => {
        if (!validateFile(file)) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            dropzone.classList.add('is-uploading');

            const response = await fetch('/upload/', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Ошибка сервера: ${response.status}`);
            }

            const data = await response.json();

            if (currentUploadInput) {
                currentUploadInput.value = data.url;
            }

            alert('Файл успешно загружен!');
        } catch (err) {
            console.error('Ошибка загрузки:', err);
            alert('Не удалось загрузить файл. Попробуйте ещё раз.');
        } finally {
            dropzone.classList.remove('is-uploading');
        }
    };

    // Выбор файла через системный диалог
    fileUpload.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) uploadFile(file);
        event.target.value = '';
    });

    // Drag & drop — единый обработчик вместо дублирования
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
        });
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => {
            dropzone.classList.add('is-dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => {
            dropzone.classList.remove('is-dragover');
        });
    });

    dropzone.addEventListener('drop', (event) => {
        const file = event.dataTransfer.files[0];
        if (file) uploadFile(file);
    });
});