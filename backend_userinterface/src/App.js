import React from 'react';
import Form from "./components/Form";
import './App.css';
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

function App() {
  return (<Router>
      <div className="App">
        <div className="auth-wrapper">
          <div className="auth-inner">
            <Switch>
              <Route exact path='/' component={Form} />
              <Route path="/sign-in" component={Form} />
            </Switch>
          </div>
        </div>
      </div></Router>
  );
}

export default App;
