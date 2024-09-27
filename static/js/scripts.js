document.addEventListener('DOMContentLoaded', () => {
    const nome = document.querySelector('#nome');
    const descricao = document.querySelector('#descricao');
    const btEnviar = document.querySelector("#btnEnviar");
    const btAdicionarCampo = document.querySelector('#btnAddField');
    const form = document.querySelector('#formulario');
    const perguntasDiv = document.querySelector('#perguntas');
    const editar = window.location.pathname.includes('/editar')
    const perguntas = [];

    const addPergunta = () => {
        const div = document.createElement('div');
        div.classList.add('input-container');

        const pergunta = document.createElement('input');
        pergunta.type = 'text';
        pergunta.placeholder = 'Enunciado da Pergunta';
        div.appendChild(pergunta);

        const selecao = document.createElement('select');
        const opcoes = [
            { value: 'text', text: 'Resposta curta' },
            { value: 'textarea', text: 'Resposta longa' },
            { value: 'radio', text: 'Múltipla escolha' },
            { value: 'checkbox', text: 'Checkbox' }
        ];

        opcoes.forEach(opcao => {
            const optionElement = document.createElement('option');
            optionElement.value = opcao.value;
            optionElement.text = opcao.text;
            selecao.appendChild(optionElement);
        });

        div.appendChild(selecao);

        const alternativasContainer = document.createElement('div');
        div.appendChild(alternativasContainer);

        selecao.addEventListener('change', () => {
            alternativasContainer.innerHTML = '';
            if (selecao.value === 'radio' || selecao.value === 'checkbox') {
                const addAltBtn = document.createElement('button');
                addAltBtn.textContent = 'Adicionar Alternativa';
                alternativasContainer.appendChild(addAltBtn);

                addAltBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    const alternativaInput = document.createElement('input');
                    alternativaInput.type = 'text';
                    alternativaInput.placeholder = 'Alternativa';
                    alternativasContainer.appendChild(alternativaInput);
                });
            }
        });

        perguntasDiv.appendChild(div);
    };

    btAdicionarCampo.addEventListener('click', addPergunta);

    btEnviar.addEventListener('click', (e) => {
        e.preventDefault();

        const perguntasArray = Array.from(perguntasDiv.children).map(perguntaDiv => {
            const texto = perguntaDiv.querySelector('input[type="text"]').value;
            const tipo = perguntaDiv.querySelector('select').value;
            const alternativas = Array.from(perguntaDiv.querySelectorAll('input[placeholder="Alternativa"]')).map(alt => alt.value);
            return { texto, tipo, alternativas };
        });

        const formData = {
            nome: nome.value,
            descricao: descricao.value,
            perguntas: perguntasArray
        };

        const url = editar ? window.location.pathname : '/submit'
        axios.post(url, formData)
            .then(response => {
                if (response.data.success){
                    const formId = response.data.form_id;
                    alert("Formulário criado com sucesso!")
                    window.location.href =  `/formulario/${formId}`;
                }else{
                    alert(response.data.error);
                };
            })
            .catch(error => {
                console.error(error.response.data);
            });
    });
});
