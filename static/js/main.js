// Show/hide form fields based on complaint type
document.addEventListener('DOMContentLoaded', function() {
    const complaintType = document.getElementById('id_complaint_type');
    const roomNumberField = document.getElementById('id_room_number').parentElement;
    const departmentField = document.getElementById('id_department').parentElement;
    const facultyNameField = document.getElementById('id_faculty_name').parentElement;
    const libraryIssueField = document.getElementById('id_library_issue_type').parentElement;
    const bookNameField = document.getElementById('id_book_name').parentElement;
    
    function toggleFields() {
        const type = complaintType.value;
        
        // Hide all fields first
        roomNumberField.style.display = 'none';
        departmentField.style.display = 'none';
        facultyNameField.style.display = 'none';
        libraryIssueField.style.display = 'none';
        bookNameField.style.display = 'none';
        
        // Show relevant fields based on complaint type
        if (type === 'hostel') {
            roomNumberField.style.display = 'block';
        } else if (type === 'faculty') {
            departmentField.style.display = 'block';
            facultyNameField.style.display = 'block';
        } else if (type === 'library') {
            libraryIssueField.style.display = 'block';
            
            // Show book name field only if book not found is selected
            const libraryIssueType = document.getElementById('id_library_issue_type');
            if (libraryIssueType && libraryIssueType.value === 'book_not_found') {
                bookNameField.style.display = 'block';
            }
        }
    }
    
    // Initial toggle
    toggleFields();
    
    // Add event listeners
    if (complaintType) {
        complaintType.addEventListener('change', toggleFields);
    }
    
    const libraryIssueType = document.getElementById('id_library_issue_type');
    if (libraryIssueType) {
        libraryIssueType.addEventListener('change', function() {
            if (this.value === 'book_not_found') {
                bookNameField.style.display = 'block';
            } else {
                bookNameField.style.display = 'none';
            }
        });
    }
});