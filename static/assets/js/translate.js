function loadGoogleTranslate() {
    // Clear any previous Google Translate elements in the div
    var googleElement = document.getElementById('google_element');
    googleElement.innerHTML = ''; // Clear previous instance

    // Now initialize Google Translate
    new google.translate.TranslateElement({
        // pageLanguage: 'en',
        includedLanguages: 'fa,tr,ar,en', // Persian (fa), Turkish (tr), Arabic (ar)
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
        autoDisplay: false,
        callback: function() {
            // After translation, get the current language
            var lang = google.translate.TranslateElement.prototype.getLang();
            
            // Force language-specific direction changes
            if (lang === 'fa' || lang === 'ar') {
                document.documentElement.setAttribute('dir', 'rtl');  // Set the page direction to RTL
                document.body.setAttribute('dir', 'rtl');
                // Force the text alignment to be RTL (Right to Left)
                document.body.style.textAlign = 'right';
            } else {
                document.documentElement.setAttribute('dir', 'ltr');  // Set the page direction to LTR
                document.body.setAttribute('dir', 'ltr');
                // Force the text alignment to be LTR (Left to Right)
                document.body.style.textAlign = 'left';
            }
        }
    }, 'google_element');
}

// Dynamically load Google Translate script
(function() {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://translate.google.com/translate_a/element.js?cb=loadGoogleTranslate';
    document.body.appendChild(script);
})();