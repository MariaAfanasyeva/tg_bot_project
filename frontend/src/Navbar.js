import React, { Component } from "react";
import {Link} from "react-router-dom";

class Navbar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            categories: [],
            error: null
        }

    }

    componentDidMount() {
        fetch('/api/category').then(res => res.json()).then(
            (result) => {
                this.setState({
                    categories: result
                });
            },
            (error) => {
                this.setState({
                   error
                });
            }
        )
    }

    render() {
        const {error, categories} = this.state;
        if (error) {
            return <p>Error {error.message}</p>
        } else {
            return (
                <div>
                    <nav className="navbar navbar-expand-lg navbar-light bg-light">
                        <a className="navbar-brand" href="#">Navbar</a>
                        <button className="navbar-toggler" type="button" data-toggle="collapse"
                            data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false"
                            aria-label="Toggle navigation">
                            <span className="navbar-toggler-icon"></span>
                        </button>
                        <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
                            <div className="navbar-nav">
                                {categories.map(category => (
                                    <Link className="nav-item nav-link" to={{pathname: `/category/${category.id}`, fromDashboard: false}}>{category.name}</Link>
                                ))}
                            </div>
                        </div>
                    </nav>
                </div>
            );
        }
    }
}

export default Navbar;