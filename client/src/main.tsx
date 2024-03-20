import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'  
import { ApolloClient, InMemoryCache, ApolloProvider } from "@apollo/client";


const URL_QUERY_GRAPHQL = "http://localhost:4000/graphql";

const client = new ApolloClient({
    uri: URL_QUERY_GRAPHQL,
    cache: new InMemoryCache(),
});



ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
