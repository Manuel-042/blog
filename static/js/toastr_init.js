toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "positionClass": "toast-top-right",
    "timeOut": "5000",
    "progressBar": true
};

// {% if messages %}
//     {% for message in messages %}
//         toastr.{{ message.tags }}("{{ message.message }}");
//     {% endfor %}
// {% endif %}