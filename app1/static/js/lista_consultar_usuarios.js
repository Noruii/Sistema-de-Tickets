let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: 'centered', targets: [0, 1, 2, 3, 4, 5, 6, 7, 8]},
        { orderable: false, targets: [8]},
        // { searchable: false, targets: [0]}
    ],
    language: {
        "decimal": "",
        "emptyTable": "Aún no se han creado usuarios.",
        "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
        
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

    // await listUsuarios();

    dataTable = $('#datatable-usuarios').DataTable(dataTableOptions);
    
    dataTableIsInitialized = true;
}

// const listUsuarios = async()=>{
//     try {
//         const response = await fetch('http://127.0.0.1:8000/lista_panel/')
//         // ngrok
//         // const response = await fetch('https://2463-179-52-24-32.ngrok.io/lista_panel/')
//         const data = await response.json();
        

//         let content = ``;
//         data.usuarios.forEach((usuario, index) => {

//             content += `
//                 <tr>
//                     <td>${index+1}</td>
//                     <td>${usuario.id}</td>
//                     <td>${usuario.is_superuser}</td>
//                     <td>${usuario.is_staff}</td>
//                     <td>${usuario.username}</td>
//                     <td>${usuario.email}</td>
//                     <td>${usuario.is_active}</td>
//                     <td>${usuario.first_name}</td>
//                     <td>${usuario.last_name}</td>
//                     <td>
//                         <a href="#" class="btn btn-sm btn-info"><i class='fa fa-solid fa-pencil'></i></a>

//                         <a href="#" onclick="eliminar_usuario(${ usuario.id })" class='btn btn-sm btn-danger'><i class='fa fa-solid fa-trash'></i></a>
//                     </td>

//                 </tr>
//             `;

//         });
//         tableBody_consultar_usuarios.innerHTML = content;

//     } catch (error) {
//         alert(error)
//     }
// };

window.addEventListener('load', async()=>{
    await initDataTable();
});