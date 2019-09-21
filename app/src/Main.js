import React, { Component } from "react";
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import Dashboard from "./Dashboard";
import History from "./History";
import Crushing from "./Crush";
import Pricing from "./Price";


class Main extends Component {
  render() {
    return (
      <HashRouter>
        <div>
          <h1>sdthon</h1>
          <ul className="header">
            <li><NavLink exact to="/">Dashboard</NavLink></li>
            <li><NavLink to="/History">History</NavLink></li>
            <li><NavLink to="/Crush">Crushing</NavLink></li>
            <li><NavLink to="/price">Pricing</NavLink></li>
          </ul>
          <div className="content">
            <Route exact path="/" component={Dashboard}/>
            <Route path="/History" component={History}/>
            <Route path="/Crush" component={Crushing}/>
            <Route path="/Price" component={Pricing}/>
          </div>
        </div>
      </HashRouter>
    );
  }
}

export default Main;
