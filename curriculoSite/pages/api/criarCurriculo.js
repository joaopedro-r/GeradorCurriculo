// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import axios from 'axios'

export default async function handler(req, res) {
  //tipo post
  if(req.method === 'POST'){
    const {usuario, senha} = req.body
    const response = await axios.post('http://127.0.0.1:8080/curriculo/create',
    {
      "usuario": usuario,
      "senha": senha
    }).then((response) => {
      res.status(200).json(response.data)
    }).catch((error) => {
        res.status(500).json({error: 'Erro ao criar curriculo'})
    });
  }

}




