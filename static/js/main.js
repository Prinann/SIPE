document.addEventListener('DOMContentLoaded', () => {
    const campoBusca = document.getElementById('campo-busca');
    const resultadosBuscaDiv = document.getElementById('resultados-busca');
    const secoesProcuracoes = document.querySelectorAll('h3.mt-4, .table-responsive, p');

    const buscarProcuracoes = async (query) => {
        if (query.length < 2) {
            resultadosBuscaDiv.innerHTML = '';
            resultadosBuscaDiv.style.display = 'none';
            secoesProcuracoes.forEach(el => el.style.display = 'block');
            return;
        }

        resultadosBuscaDiv.style.display = 'block';
        secoesProcuracoes.forEach(el => el.style.display = 'none');

        try {
            const response = await fetch(`/api/buscar/?q=${query}`);
            const data = await response.json();

            let html = '<h3>Resultados da Busca</h3>';
            if (data.procuracoes.length > 0) {
                html += `<div class="table-responsive">
                            <table class="table table-striped table-bordered">
                                <thead class="table-primary text-white">
                                    <tr>
                                        <th>Outorgante</th>
                                        <th>Outorgado</th>
                                        <th>Data de Vencimento</th>
                                    </tr>
                                </thead>
                                <tbody>`;
                data.procuracoes.forEach(proc => {
                    const dataVencimento = new Date(proc.data_vencimento).toLocaleDateString('pt-BR');
                    html += `<tr>
                                <td>${proc.outorgante}</td>
                                <td>${proc.outorgado}</td>
                                <td>${dataVencimento}</td>
                            </tr>`;
                });
                html += `       </tbody>
                            </table>
                        </div>`;
            } else {
                html += '<p>Nenhuma procuração encontrada.</p>';
            }

            resultadosBuscaDiv.innerHTML = html;

        } catch (error) {
            console.error('Erro ao buscar procurações:', error);
            resultadosBuscaDiv.innerHTML = '<p class="text-danger">Ocorreu um erro na busca.</p>';
        }
    };

    campoBusca.addEventListener('input', (event) => {
        const query = event.target.value;
        buscarProcuracoes(query);
    });
});

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("btn-topo").style.display = "block";
  } else {
    document.getElementById("btn-topo").style.display = "none";
  }
}

function topFunction() {
  document.body.scrollTop = 0; // Para Safari
  document.documentElement.scrollTop = 0; // Para Chrome, Firefox, IE e Opera
}