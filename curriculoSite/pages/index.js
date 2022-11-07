import { Col,Row, Container,Image, Button,Form,Spinner  } from 'react-bootstrap';
import Head from 'next/head'
import styles from '../styles/Home.module.css'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios';
import dadosCurriculo from './globals'

export default function Home() {
    const [login, setLogin] = useState('')
    const [senha, setSenha] = useState('')
    const [loading, setLoading] = useState(false)
    const router = useRouter()
    
    

    const criarCurriculo = async () => {
        
        setLoading(true)
        const response = await axios.post('http://localhost:3000/api/criarCurriculo', {
            "usuario": login,
            "senha": senha,
        }).then((response) => {
            const _dados = response.data
            dadosCurriculo = _dados
            router.push('/curriculo')
        }).catch((error) => {
            alert('Erro ao criar curriculo')
            setLoading(false) 
        });        
      };

    return (
        <div>
            <Head>
                <title>Home</title>
            </Head>
            <main id={styles.corpoPrincipal}>
                {loading == true ?
                <div className={styles.spinnerCenter}>
                    <Spinner animation="border" role="status" >
                    </Spinner>
                    <p>Gerando currículo</p>
                    <p>Este precesso pode levar alguns minutos</p>
                </div>
                :
                <Container className={styles.central}>
                    <h1>CURRÍCULO CREATOR</h1>
                    <p className={styles.paragrafo}>Este site foi criado para facilitar a criação de curriculos a partir do LinkedIn.</p>
                    <p className={styles.paragrafo}>Para começar insira seu login do LinkedIn</p>

                    <Form className={styles.formulario} >
                        <Form.Group controlId="formBasicEmail" className="mb-3">
                            <Form.Label>Login do LinkedIn</Form.Label>
                            <Form.Control type="email" placeholder="Insira seu e-mail do LinkedIn"  onChange={(a)=>setLogin(a.target.value)} />
                            <Form.Text className="text-muted">
                            Nós nunca compartilharemos seu email com ninguém.
                            </Form.Text>
                        </Form.Group>
                        <Form.Group controlId="formBasicPassword">
                            <Form.Label>Senha</Form.Label>
                            <Form.Control type="password" placeholder="Insira sua senha" onChange={(a)=>setSenha(a.target.value)}/>
                        </Form.Group>
                    </Form>
                        <div id={styles.botaoCriar}>
                            <Button variant="light" onClick={(a)=>criarCurriculo()}>CRIAR CURRÍCULO</Button>
                        </div>
                </Container>
                }
            </main>
            
        </div>
    )
}