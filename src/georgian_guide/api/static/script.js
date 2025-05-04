document.addEventListener('DOMContentLoaded', function() {
    const queryForm = document.getElementById('queryForm');
    const queryInput = document.getElementById('query');
    const submitBtn = document.getElementById('submitBtn');
    const loader = document.getElementById('loader');
    const responseContainer = document.getElementById('responseContainer');
    const responseContent = document.getElementById('responseContent');
    const followUpContainer = document.getElementById('followUpContainer');
    const followUpList = document.getElementById('followUpList');
    const exampleButtons = document.querySelectorAll('.example-btn');

    // Handle form submission
    queryForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const query = queryInput.value.trim();
        
        if (query) {
            sendQuery(query);
        }
    });

    // Handle example button clicks
    exampleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const query = this.getAttribute('data-query');
            queryInput.value = query;
            sendQuery(query);
        });
    });

    // Handle follow-up question clicks
    followUpList.addEventListener('click', function(e) {
        if (e.target.tagName === 'LI') {
            const query = e.target.textContent;
            queryInput.value = query;
            sendQuery(query);
        }
    });

    // Function to send query to API
    function sendQuery(query) {
        // Show loader, disable submit button
        loader.style.display = 'block';
        submitBtn.disabled = true;
        
        // Hide previous response if any
        responseContainer.style.display = 'none';
        
        // Prepare the request
        const url = `/api/ask?query=${encodeURIComponent(query)}`;
        
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                displayResponse(data);
            })
            .catch(error => {
                displayError(error);
            })
            .finally(() => {
                // Hide loader, enable submit button
                loader.style.display = 'none';
                submitBtn.disabled = false;
            });
    }

    // Function to display the API response
    function displayResponse(data) {
        // Display the main response
        responseContent.textContent = data.response;
        
        // Display follow-up questions if any
        if (data.follow_up_questions && data.follow_up_questions.length > 0) {
            followUpList.innerHTML = '';
            data.follow_up_questions.forEach(question => {
                const li = document.createElement('li');
                li.textContent = question;
                followUpList.appendChild(li);
            });
            followUpContainer.style.display = 'block';
        } else {
            followUpContainer.style.display = 'none';
        }
        
        // Show the response container
        responseContainer.style.display = 'block';
        
        // Scroll to the response
        responseContainer.scrollIntoView({ behavior: 'smooth' });
    }

    // Function to display errors
    function displayError(error) {
        responseContent.textContent = `Error: ${error.message}. Please try again.`;
        followUpContainer.style.display = 'none';
        responseContainer.style.display = 'block';
    }
}); 