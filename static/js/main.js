// Smart Farmer Custom JavaScript
document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss alert messages after 6 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 6000);
    });
});
