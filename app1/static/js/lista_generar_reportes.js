$("#datatable-generar-reportes").DataTable({
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5] },
        { searchable: false, targets: [0] },
    ],
    language: {
        decimal: "",
        emptyTable: "Aún no se ha creado ningún ticket.",
        info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
        infoEmpty: "Mostrando 0 Tickets de 0 de 0 Entradas",
        infoFiltered: "(Filtrado de _MAX_ total entradas)",
        infoPostFix: "",
        thousands: ",",
        lengthMenu: "Mostrar _MENU_ Entradas",
        loadingRecords: "Cargando...",
        processing: "Procesando...",
        search: "Buscar:",
        zeroRecords: "Sin resultados encontrados",
        paginate: {
            first: "Primero",
            last: "Ultimo",
            next: "Siguiente",
            previous: "Anterior",
        },
    },
    pageLength: 10,
    destroy: true,
    responsive: true,
    dom: 'Bfrtip',
    buttons: [
        {
            extend: 'excelHtml5',
            text: '<i class="fas fa-solid fa-file-excel"></i> ',
            titleAttr: 'Exportar a Excel',
            className: 'btn btn-outline-success',
        },
        {
            extend: 'pdfHtml5',
            text: '<i class="fas fa-regular fa-file-pdf"></i> ',
            titleAttr: 'Exportar a PDF',
            className: 'btn btn-outline-danger',
            download: 'open',
            orientation: 'landscape',
            pageSize: 'LEGAL',
            customize: function (doc) {
                doc.styles = {
                    header: {
                        fontSize: 18,
                        bold: true,
                        alignment: 'center'
                    },
                    subheader: {
                        fontSize: 13,
                        bold: true
                    },
                    quote: {
                        italics: true
                    },
                    small: {
                        fontSize: 8
                    }, 
                    tableHeader: {
                        bold: true,
                        fontSize: 11,
                        color: 'white',
                        fillColor: '#48e',
                        alignment: 'center'
                    }
                };
                doc.content[1].table.widths = ['20%', '20%', '15%','15%', '15%', '15%'];
                doc.content[1].margin = [0, 35, 0, 0];
                doc.content[1].layout = {};
                doc['footer'] = (function (page, pages) {
                    return {
                        columns: [
                            {
                                //alignment: 'left',
                            },
                            {
                                alignment: 'right',
                                text: ['pagina ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                            }
                        ],
                        margin: 20
                    }
                });
            }
            
        },
        {
            extend: 'print',
            text: '<i class="fa fa-print"></i> ',
            titleAttr: 'Imprimir',
            className: 'btn btn-outline-info',
        },
    ]
});
