import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import axios from 'axios';

class PdfToWord extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            isVisible: false,
            tableStartPage: '',
            tableEndPage: '',
            paragraphStartPage: '',
            paragraphEndPage: '',
            downloadFile: null
        }
    }

    handleChange=event=> {
        this.setState({
            [event.target.name]: event.target.value
        })
        console.log(this.state.tableStartPage)
    }

    handleFileUpdate=(uploadedFile)=> {
        this.setState(state=>({
            downloadFile: uploadedFile,
            isVisible: true
        }))
    }

    render() {
        return (
            <div>
                <h1>PDFToWord WebApp</h1>
                <FileDropBox mainHandleChange={this.handleChange}
                updateFile={this.handleFileUpdate} 
                start={this.state.tableStartPage}
                end={this.state.tableEndPage} 
                s={this.state.paragraphStartPage} 
                e={this.state.paragraphEndPage}/>
                {this.state.isVisible && 
                <InputTable
                fileToBeDownload={this.state.downloadFile}/>}
            </div>
        )
    }
}

class InputTable extends React.Component {
    constructor(props) {
        super(props)
    }

    triggerDownload=()=>{
        console.log(this.props.fileToBeDownload)
        const url = window.URL.createObjectURL(new Blob([this.props.fileToBeDownload]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'output.docx');
        document.body.appendChild(link);
        link.click();
    }

    render() {
        return(
            <div> 
                <div>
                    <p> download file clicking the button below</p> 
                </div> 
                <div>
                    <button onClick={this.triggerDownload}>Download</button>
                </div>
            </div>
        )
    }
}

class FileDropBox extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            isDisplayed: false,
            selectedFile: null,
            time: ''
        }
    }

    onChangeHandler=event=>{
        this.setState({
            selectedFile: event.target.files[0]
        })
        console.log(event.target.files[0])
    }

    handleSubmit=event=> {
        event.preventDefault()
        const data = new FormData()
        data.append('data', this.state.selectedFile)
        data.append('tableStartPage', this.props.start)
        data.append('tableEndPage', this.props.end)
        data.append('paragraphStartPage', this.props.s)
        data.append('paragraphEndPage', this.props.e)
        axios.post("http://localhost:3000/upload", data)
        .then(res=>{
            this.props.updateFile(res.data)
        })

        {/*}
        fetch('/time').then(res=>res.json()).then(data=>{
            this.setState({time:data.time})
        })
        this.setState({
            isDisplayed: true
        })
        */}
    }

    render() {
        return(
            <div className="container">
                <div className="box">
                    <label>Upload your file</label>
                    <input type="file" onChange={this.onChangeHandler}/>
                </div>
                {this.state.isDisplayed &&
                    <textarea value={this.state.time} />}
                    <form id="fileUpload" onSubmit={this.handleSubmit}>
                        <div>
                            <label>
                                table starting page number:
                                <input type="text" className="input-box" name="tableStartPage" value={this.props.start} onChange={this.props.mainHandleChange} />
                            </label>
                        </div>
                        <div>
                            <label>
                                table ending page number:
                                <input type="text" className="input-box" name = "tableEndPage" value={this.props.end} onChange={this.props.mainHandleChange} />
                            </label>
                        </div>
                        <div>
                            <label>
                                text starting page number:
                                <input type="text" className="input-box" name="paragraphStartPage" value={this.props.s} onChange={this.props.mainHandleChange} />
                            </label>
                        </div>
                        <div>
                            <label>
                                text ending page number:
                                <input type="text" className="input-box" name="paragraphEndPage" value={this.props.e} onChange={this.props.mainHandleChange} />
                            </label>
                        </div>
                    </form>
                <button form="fileUpload" type="submit">Upload</button>
            </div>
        )
    }
}
// ========================================

ReactDOM.render(
  <PdfToWord />,
  document.getElementById('root')
);
