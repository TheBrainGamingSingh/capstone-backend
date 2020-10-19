import React, { Component } from "react";
import DisplayCategory from './displayCategory.js'

export default class Form extends Component {
    constructor(props) {
        super(props);
        this.state = {
          complaintText: '',
          toClassifier: false
        };
      }
      mySubmitHandler = (event) => {
        event.preventDefault();
        console.log(this.state.complaintText);
        this.setState({toClassifier: true});
      }
      myChangeHandler = (event) => {
        this.setState({complaintText: event.target.value});
      }
    render() {
        const toClassifier = this.state.toClassifier;
        if (toClassifier) {
            return <DisplayCategory complaintText = {this.state.complaintText}/>
        }
        return (
            <div>
    <form onSubmit={this.mySubmitHandler}>
      <h1>Complaint Submission</h1>
      <p>Enter your complaint:</p>
      <input
        type='text'
        name='complaintText'
        onChange={this.myChangeHandler}
      />
      <br/>
      <br/>
      <input type='submit' />
      </form>
      </div>
        );
    }
}