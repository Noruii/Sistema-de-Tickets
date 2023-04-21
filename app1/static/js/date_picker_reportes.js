// $(function () {
//     $('input[name="dates"]').daterangepicker({
//         locale: {
//             format: "DD-MM-YYYY",
//             separator: " - ",
//             applyLabel: "Aplicar",
//             cancelLabel: "Cancelar",
//             fromLabel: "Desde",
//             toLabel: "Hasta",
//             customRangeLabel: "Personalizar",
//             daysOfWeek: [
//                 "Do",
//                 "Lu",
//                 "Ma",
//                 "Mi",
//                 "Ju",
//                 "Vi",
//                 "Sa"
//             ],
//             monthNames: [
//                 "Enero",
//                 "Febrero",
//                 "Marzo",
//                 "Abril",
//                 "Mayo",
//                 "Junio",
//                 "Julio",
//                 "Agosto",
//                 "Setiembre",
//                 "Octubre",
//                 "Noviembre",
//                 "Diciembre"
//             ],
//             "firstDay": 1
//         },
//         opens: "center",
//         cancelButtonClasses: 'btn-danger'
//     });
// });

$(function () {
    $('input[name="dates"]').daterangepicker({
        locale: {
            format: "DD-MM-YYYY",
            separator: " - ",
            applyLabel: "Seleccionar",
            cancelLabel: "Cancelar",
            fromLabel: "Desde",
            toLabel: "Hasta",
            customRangeLabel: "Personalizar",
            daysOfWeek: [
                "Do",
                "Lu",
                "Ma",
                "Mi",
                "Ju",
                "Vi",
                "Sa"
            ],
            monthNames: [
                "Enero",
                "Febrero",
                "Marzo",
                "Abril",
                "Mayo",
                "Junio",
                "Julio",
                "Agosto",
                "Setiembre",
                "Octubre",
                "Noviembre",
                "Diciembre"
            ],
            "firstDay": 1
        },
        opens: "center",
        cancelButtonClasses: 'btn-danger'
    });
    // .on('apply.daterangepicker', function(ev, picker) {

    //     console.log(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'))
    // }).on('cancel.daterangepicker', function(ev, picker) {

    //     console.log(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'))
    // });
});