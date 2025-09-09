document.addEventListener('DOMContentLoaded', () => {
    const campoBusca = document.getElementById('campo-busca');
    const resultadosBuscaDiv = document.getElementById('resultados-busca');
    const listasProcuracoes = document.querySelectorAll('h3, ul');

    const buscarProcuracoes = async (query) => {
        if (query.length < 2) {
            // Esconde os resultados da busca se a query for muito curta
            resultadosBuscaDiv.innerHTML = '';
            resultadosBuscaDiv.style.display = 'none';
            listasProcuracoes.forEach(el => el.style.display = 'block');
            return;
        }

        // Exibe a div de resultados e esconde as listas de alerta
        resultadosBuscaDiv.style.display = 'block';
        listasProcuracoes.forEach(el => el.style.display = 'none');

        try {
            // Faz a requisição para a nossa API
            const response = await fetch(`/api/buscar/?q=${query}`);
            const data = await response.json();

            // Monta o HTML com os resultados
            let html = '<h3>Resultados da Busca</h3>';
            if (data.procuracoes.length > 0) {
                html += '<ul>';
                data.procuracoes.forEach(proc => {
                    const dataVencimento = new Date(proc.data_vencimento).toLocaleDateString('pt-BR');
                    html += `<li>${proc.outorgante} - Vence em ${dataVencimento}</li>`;
                });
                html += '</ul>';
            } else {
                html += '<p>Nenhuma procuração encontrada.</p>';
            }

            resultadosBuscaDiv.innerHTML = html;

        } catch (error) {
            console.error('Erro ao buscar procurações:', error);
            resultadosBuscaDiv.innerHTML = '<p class="mensagem-erro">Ocorreu um erro na busca.</p>';
        }
    };

    // Adiciona um "ouvinte" ao campo de busca
    campoBusca.addEventListener('input', (event) => {
        const query = event.target.value;
        buscarProcuracoes(query);
    });
});