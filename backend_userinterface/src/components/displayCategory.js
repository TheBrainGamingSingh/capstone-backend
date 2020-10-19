import React, { Component } from "react";

export default class DisplayCategory extends Component {
    constructor(props) {
        super(props);
        this.state = {
          complaintCategory: '',
          confidence: 0,
          complaintText: this.props.complaintText
        };
      }

      componentDidMount() {
        const apiUrl = 'http://127.0.0.1:5000/predict/query=' + this.state.complaintText;
        fetch(apiUrl)
          .then((response) => response.json())
          .then((data) => { 
            console.log(data);
            const prediction = data.prediction;
            const confid = data.confidence;
            this.setState({complaintCategory: prediction, confidence: confid});
          });
      }
      
    render() {
        return (
    <div>
      <h1>Complaint Submission</h1>
      <p>{this.state.complaintText}</p>
      <h2>Category: </h2>
      <p>{this.state.complaintCategory}</p>
      </div>
        );
    }
}