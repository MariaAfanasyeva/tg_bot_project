import React, { Component } from "react";

class BotsList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            items: [],
            isSelected: false,
            selectedItems: []
        };

        this.handleClick = this.handleClick.bind(this);
    }
    handleClick(item, event) {
        event.preventDefault();
        if (this.state.selectedItems.includes(item.id)) {
            const index = this.state.selectedItems.indexOf(item.id);
            delete this.state.selectedItems[index];
            this.setState(state => {
                return {
                    isSelected: !this.state.isSelected,
                    selectedItems: this.state.selectedItems,
                }
            });
        } else {
            this.setState(state => {
                return {
                    isSelected: !this.state.isSelected,
                    selectedItems: [this.state.selectedItems, item.id],
                }
            });
        }
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
        const {error, isLoaded, items, selectedItems} = this.state;
        if (error) {
            return <p>Error {error.message}</p>
        } else if (!isLoaded) {
            return <p>Loading...</p>
        } else if (!selectedItems) {
            return (
                <ul>
                    {items.map(item =>
                        <li key={item.id}>
                            <a id={item.id} onClick={(event) => this.handleClick(item, event)}>{item.name}</a>
                        </li>
                    )}
                </ul>
            );
        } else {
            return (
                <ul>
                    {items.map((item) => ( (selectedItems.includes(item.id)) ?
                        <li id={item.name}>
                            <a id={item.id} onClick={(event) => this.handleClick(item, event)}>{item.name}</a>
                            <p>{item.description}</p>
                        </li> : <li id={item.name}>
                            <a id={item.id} onClick={(event) => this.handleClick(item, event)}>{item.name}</a>
                        </li>
                    ))}
                </ul>
            )
        }
    }
}

export default BotsList;