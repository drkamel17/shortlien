function toggleCustom() {
    const checkbox = document.getElementById('useCustom');
    const customInput = document.getElementById('customCode');
    if (checkbox.checked) {
        customInput.classList.remove('hidden');
    } else {
        customInput.classList.add('hidden');
    }
}

async function shortenUrl() {
    const urlInput = document.getElementById('urlInput');
    const resultDiv = document.getElementById('result');
    const shortUrlInput = document.getElementById('shortUrl');
    const useCustom = document.getElementById('useCustom').checked;
    const customCode = document.getElementById('customCode').value.trim();
    const originalUrl = urlInput.value.trim();

    if (!originalUrl) {
        alert('الرجاء إدخال رابط');
        return;
    }

    const payload = { url: originalUrl };
    if (useCustom && customCode) {
        payload.custom_code = customCode;
    }

    try {
        const response = await fetch('/shorten', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            shortUrlInput.value = data.short_url;
            resultDiv.classList.remove('hidden');
        } else {
            alert(data.error || 'حدث خطأ');
        }
    } catch (error) {
        alert('فشل الاتصال بالخادم');
    }
}

function copyToClipboard() {
    const shortUrlInput = document.getElementById('shortUrl');
    shortUrlInput.select();
    navigator.clipboard.writeText(shortUrlInput.value);
    
    const copyBtn = document.querySelector('.copy-btn');
    copyBtn.textContent = '✅ تم النسخ';
    setTimeout(() => {
        copyBtn.textContent = 'نسخ';
    }, 2000);
}

document.getElementById('urlInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        shortenUrl();
    }
});