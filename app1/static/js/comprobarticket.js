let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    scrollY: "400px",
    lengthMenu: [5, 10, 15, 20, 100, 200, 500],
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6] },
        { orderable: false, targets: [5, 6] },
        { searchable: false, targets: [1] }
        //{ width: "50%", targets: [0] }
    ],
    pageLength: 50,
    destroy: true,
    language: {
        lengthMenu: "Mostrar _MENU_ tickets por página",
        zeroRecords: "Ningún usuario encontrado",
        info: "Mostrando de _START_ a _END_ de un total de _TOTAL_ tickets",
        infoEmpty: "Ningún usuario encontrado",
        infoFiltered: "(filtrados desde _MAX_ tickets totales)",
        search: "Buscar:",
        loadingRecords: "Cargando...",
        paginate: {
            first: "Primero",
            last: "Último",
            next: "Siguiente",
            previous: "Anterior"
        }
    }
};

const initDataTable = async() => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listUsers();

    dataTable = $("#datatable_users").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

const listUsers = async() => {
    try {
        const response = await fetch("https://jsonplaceholder.typicode.com/users");
        const users = await response.json();

        let content = ``;
        users.forEach((user, index) => {
            content += `
                <tr>
                    <td>${index + 1}</td>
                    <td class='nombre'>${user.name}</td>
                    <td class='titulo'>${user.email}</td>
                    <td class='email'>${user.address.city}</td>
                    <td class='categoria'>${user.company.name}</td>
                    <td><i class="fa-solid fa-check" style="color: green;"></i></td>
                    <td>
                        <button class="btn btn-sm btn-primary btnver" onclick=''>ver</button>
                        <button class="btn btn-sm btn-danger"><i class="fa-solid fa-trash-can"></i></button>
                    </td>
                </tr>`;
        });
        tableBody_users.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

try {
    window.addEventListener("load", async() => {
        await initDataTable();

        const promesa = new Promise((resolver) => {
            resolver(() => {
                const btnVerTicket = document.querySelectorAll('.btnver');
            })
        })
        promesa.then(res => {
            //informaciones de los usuarios para comentar tickets

            const btnVerTicket = document.querySelectorAll('.btnver');
            const nombre = document.querySelector('.user_name_info');
            const categoria = document.querySelector('.user_categoria');
            const fecha = document.querySelector('.user_fechaticket');
            const estado = document.querySelector('.user_estadoticket');
            const tituloAsunto = document.querySelector('.titulo_user')


            btnVerTicket.forEach((btn, index) => {
                btn.addEventListener('click', () => {
                    index;
                    console.log(index)
                    container_user_comentario.style.display = 'grid';

                    nombre.textContent = document.querySelectorAll('.nombre')[index].textContent;
                    categoria.textContent = document.querySelectorAll('.categoria')[index].textContent;
                    //nombre.textContent = document.querySelectorAll('.titulo')[index].textContent; la fecha
                    //nombre.textContent = document.querySelectorAll('.titulo')[index].textContent; el estado
                    tituloAsunto.textContent = document.querySelectorAll('.titulo')[index].textContent;


                })

            })

        })
    });

} catch (e) {
    console.log(e)
}

//comentar tickets
const container_user_comentario = document.querySelector('.container_responder_tickets');
const btn_cancelar_ticket = document.querySelector('.btn-cancelar_ticket');

btn_cancelar_ticket.addEventListener('click', (e) => {
    e.preventDefault()
    container_user_comentario.style.display = 'none';
    setTimeout(() => {
        const boxConmentario = document.querySelector('.comentario_user');
        boxConmentario.value = '';
    }, 2000)
})