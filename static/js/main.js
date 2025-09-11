document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const filtroStatus = document.getElementById('filtroStatus');
    const cards = document.querySelectorAll('#procuracoesList .card');

    function filtrarCards() {
        const statusSelecionado = filtroStatus.value.toLowerCase();
        const textoBusca = searchInput.value.trim().toLowerCase();

        cards.forEach(card => {
            const statusCard = card.dataset.status.toLowerCase();
            const conteudo = card.innerText.toLowerCase();

            const atendeStatus = !statusSelecionado || statusCard === statusSelecionado;
            const atendeBusca = !textoBusca || conteudo.includes(textoBusca);

            if (atendeStatus && atendeBusca) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    filtroStatus.addEventListener('change', filtrarCards);
    searchInput.addEventListener('input', filtrarCards);

    // Botão voltar ao topo
    const btnTopo = document.getElementById('btn-topo');
    if (btnTopo) {
        window.onscroll = function() {
            if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                btnTopo.style.display = 'block';
            } else {
                btnTopo.style.display = 'none';
            }
        };
        btnTopo.addEventListener('click', () => {
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        });
    }
});
