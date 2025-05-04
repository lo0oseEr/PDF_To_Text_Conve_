let uploadedFile = null;

// Handle drag and drop
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const downloadBtn = document.getElementById('downloadBtn');
const previewSection = document.getElementById('previewSection');
const textPreview = document.getElementById('textPreview');

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#764ba2';
    dropZone.style.backgroundColor = '#f8f9fa';
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#ccc';
    dropZone.style.backgroundColor = 'transparent';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#ccc';
    dropZone.style.backgroundColor = 'transparent';
    
    const files = e.dataTransfer.files;
    handleFiles(files);
});

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

function handleFiles(files) {
    if (files.length > 0) {
        const file = files[0];
        if (file.type === 'application/pdf') {
            if (file.size <= 10 * 1024 * 1024) { // 10MB limit
                uploadedFile = file;
                fileName.textContent = file.name;
                fileName.style.color = '#28a745';
            } else {
                alert('File size exceeds 10MB limit');
            }
        } else {
            alert('Please upload a PDF file');
        }
    }
}

async function convertPDF() {
    if (!uploadedFile) {
        alert('Please select a PDF file first');
        return;
    }

    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        
        if (response.ok) {
            downloadBtn.disabled = false;
            previewSection.style.display = 'block';
            textPreview.textContent = data.preview;
            alert('File converted successfully!');
        } else {
            throw new Error(data.error || 'Conversion failed');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function downloadWord() {
    window.location.href = '/download';
} 