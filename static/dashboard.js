
async function loadSubjects() {
    try {
        const response = await fetch("http://127.0.0.1:5000/subjects");

        const subjects = await response.json();

        console.log("Bunk Smart Subjects:", subjects);

    } catch (error) {
        console.error("Error loading subjects:", error);
    }
}

loadSubjects();
