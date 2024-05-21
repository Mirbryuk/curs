import '../App.css'

function Button(params) {
  

  return (
    <button onClick={params.onclick}>{params.label}</button>
  )
}

export default Button
