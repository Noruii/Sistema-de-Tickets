let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: 'centered', targets: [0, 1, 2, 3, 4, 5, 6, 7, 8]},
        { orderable: false, targets: [8]},
        { searchable: false, targets: [0, 8]},
        
    ],
    language: {
        "decimal": "",
        "emptyTable": "Aún no se ha creado ningún ticket.",
        "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
        "infoEmpty": "Mostrando 0 Tickets de 0 de 0 Entradas",
        "infoFiltered": "(Filtrado de _MAX_ total entradas)",
        "infoPostFix": "",
        "thousands": ",",
        "lengthMenu": "Mostrar _MENU_ Entradas",
        "loadingRecords": "Cargando...",
        "processing": "Procesando...",
        "search": "Buscar:",
        "zeroRecords": "Sin resultados encontrados",
        "paginate": {
            "first": "Primero",
            "last": "Ultimo",
            "next": "Siguiente",
            "previous": "Anterior"
        }
    },
    pageLength: 10,
    destroy: true,
    responsive: true
}

const initDataTable = async()=>{
    if(dataTableIsInitialized){
        dataTable.destroy();
    }

    // await listTickets();

    dataTable = $('#datatable-consultar').DataTable(dataTableOptions);
    
    dataTableIsInitialized = true;
}

// const listTickets = async()=>{
//     try {
//         const response = await fetch('http://127.0.0.1:8000/lista_panel/')
//         const data = await response.json();

//         let content = ``;
//         data.tickets.forEach((ticket, index) => {

//             const usuario = data.usuarios.find(u => u.id === ticket.usuario_id);

//             const fecha = new Date(ticket.fecha_creacion);
//             const fecha_formateada = fecha.toLocaleString();
//             content += `
//                 <tr>
//                     <td>${index+1}</td>
//                     <td>${ticket.id}</td>
//                     <td>${fecha_formateada}</td>
//                     <td>${ticket.usuario_id} - ${usuario.username} </td>
                        
//                     <td>${ticket.asunto}</td>
//                     <td>${ticket.departamento}</td>
//                     <td>${ticket.descripcion}</td>
//                     <td>${ticket.email}</td>
//                     <td>
//                         <a href="" class="btn btn-sm btn-info disabled"><i class="fas fa-ban"></i></a>
                        
//                         <a href="#" onclick="eliminar_ticket(${ ticket.id})" class='btn btn-sm btn-danger'><i class='fa fa-solid fa-trash'></i></a>
                        
//                         <a href="/comentar_ticket/${ticket.id}" class='btn btn-sm btn-primary'><i class='fa fa-solid fa-comment'></i> Comentar</a>
//                     </td>
//                 </tr>
//             `;
//         });
//         tableBody_consultar_tickets.innerHTML = content;

//     } catch (error) {
//         // TODO: Arreglar
//         //     Oculte el alert debido a que aunque me esta todo bien me tira el esiguiente error:
//         //     ReferenceError: tableBody_consultar_tickets is not defined
//         // alert(error)
//         console.log(error)
//     }
// };

window.addEventListener('load', async()=>{
    await initDataTable();
});