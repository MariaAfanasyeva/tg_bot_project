import React, { Component } from "react";

class BotsList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            items: [],
            isSelected: false,
        };

        this.handleClick = this.handleClick.bind(this);
    }
    handleClick(event) {
        event.preventDefault();
        this.setState(state => ({
            isSelected: !this.state.isSelected
        }));
    }


    componentDidMount() {
        fetch('/api').then(res => res.json()).then(
            (result) => {
                this.setState({
                    isLoaded: true,
                    items: result
                });
            },
            (error) => {
                this.setState({
                   isLoaded: true,
                   error
                });
            }
        )
    }

    render() {
        const {error, isLoaded, items, isSelected} = this.state;
        if (error) {
            return <p>Error {error.message}</p>
        } else if (!isLoaded) {
            return <p>Loading...</p>
        } else if (!isSelected) {
            return (
                <ul>
                    {items.map(item => (
                        <li key={item.name}>
                            <a onClick={this.handleClick}>{item.name}</a>
                        </li>
                    ))}
                </ul>
            );
        } else {
            return (
                <ul>
                    {items.map(item => (
                        <li key={item.name}>
                            <a onClick={this.handleClick}>{item.name}</a> {item.description}
                        </li>
                    ))}
                </ul>
            )
        }
    }
}

export default BotsList;