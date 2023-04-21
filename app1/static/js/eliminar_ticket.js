function eliminar_ticket(id) {
    Swal.fire({
        title: "¿Está seguro?",
        text: "Esta ación no se puede deshacer.",
        icon: "warning",
        showCancelButton: true,
        cancelButtonText: "No, Cancelar",
        confirmButtonText: "Si, Eliminar",
        confirmButtonColor: "#dc3545",
        customClass: {
            confirmButton: 'btn btn-danger mr-2',
            cancelButton: 'btn btn-secondary'
        },
        buttonsStyling: false,
        showLoaderOnConfirm: true,
        preConfirm: () => {
            return new Promise((resolve, reject) => {
                setTimeout(() => {
                    resolve()
                }, 800)
            })
        }
    })
    .then(function (result) {
        if (result.isConfirmed) {
            window.location.href = "/eliminar_ticket/" + id + "/";
        }
        //else if (result.isDismissed) {
        //    Swal.fire('Changes are not saved', '', 'info')
        //}
    });
}
