function openFileWindow() {
    document.getElementById('fileInput').click(); 
}

function fileSelected(event) {
    var file = event.target.files[0];
    if (file) {
        var formData = new FormData();
        formData.append('file', file);
        document.body.innerHTML = document.body.innerHTML = `<div class="navbar">
                <a href="C:\\Brain-tumor-classification\\home.html" id="home">Home</a>
                <a href="https://github.com/VarunHari12/Brain-tumor-classification" id="GH">Github</a>
                </div>
                <h1>Loading Analysis</h1>
                <div class="loader"> 
                    <span></span> 
                    <span></span> 
                    <span></span> 
                    <span></span> 
                    <span></span> 
                    <span></span> 
                </div>
                <script src="upload.js"></script>`;
                
        console.log("sending now!!");
        fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            body: formData,
            headers: {
                "Accept": "application/json"
            }
        })
        .then(response => response.json())  // Parse the response as JSON
        .then(data => {
            console.log("got it!!!");
            console.log("Classification:", data.classification);
            console.log("Treatment Plan:", data['treatment plan']);
            
            // Store data in localStorage
            localStorage.setItem('classification', data.classification);
            localStorage.setItem('treatmentPlan', data['treatment plan']);

            // Redirect to the new page
            window.location.href = "classification.html";
        })
        .catch(error => {
            console.error("Error:", error);
        });
    } else {
        console.log("No file selected");
    }
}

