
$('document').ready(function(){

  class Maintenance {
    constructor(_id, _service, _cost){
      this.id = _id;
      this.service = _service;
      this.cost = _cost;
    }
  }

  const state = {
    service_data: []
  }


  const toggelSubmitButton = () => {
    console.log(state.service_data)
    if(state.service_data.length === 0){
      $('#service-submit').addClass('disabled')
    }else{
      $('#service-submit').removeClass('disabled')
    }
    
}


  const loadTable = () => {

    let domStr = ''
    state.service_data.forEach( obj => {
      domStr += `
        <tr>
          <td>${obj.service}</td>
          <td>GHc${obj.cost}</td>
          <td></td>
        </tr>
      `
    })
  
    const total_cost = state.service_data.reduce((prev, next) => parseInt(next.cost) + prev,0)

    $('#table-total span')[0].textContent = total_cost
    $('#maintenance-table tbody').html(domStr)

    toggelSubmitButton()
}

  const servicesIDS = () => state.service_data.map( service => service.id.slice(-1) ).join(' ').toString()

  const setServiceData = _data => {
    state.service_data = [..._data]
  }


/* printButton url changeHandler */

  const printUrlChangeHandler = (token = null) => {
    const url = $('#print-btn').attr('href').replace('token',token)
    $('#print-btn').attr('href', url)
    // console.log($('#print-btn').attr('href'))
  }



  /*** Service Selection ***/

  $.each($('.service-card'), (_, el) => {
    el.addEventListener('click', function(){
      this.classList.toggle('activated')
      var data = []

      if(this.classList.contains('activated')){
        data = [...state.service_data, new Maintenance(this.id, $(`#${this.id}  #service-text`).text(), $(`#${this.id}  #service-cost span`).text())]
      }else{
        data = state.service_data.filter( service => service.id !== this.id )
      }

      setServiceData(data)


      // printUrlChangeHandler()
      loadTable()
    })
  })




  /*** submit maintenance ***/
  // FIXME: change this url and use the hosted url during deployment
  const postUrl = 'http://127.0.0.1:8000/vehicle/customers/render/service'
  
  let notifier = new AWN();

  const postRequest = () => {
    $.ajax({
      url:postUrl,
      type:'GET',
      data:{type: 'render-service',data: servicesIDS()},
      dataType:'json',
      contentType: 'application/json',
      success: function(res){
        // console.log(res.data.token)
        notifier.info('Service rendered successfully')
        //Show print
        $('#print-btn').removeClass('d-none')
        $('#payment-btn').removeClass('d-none')
        //change print url
        printUrlChangeHandler(res.data.token);
      },
      error: function(err){
        notifier.info('Service rendered unsuccessfully, Try again!!!')
      }
    })
  }
  
  
  $('#service-submit').on('click', function(){
    let onCancel = () => {notifier.info('Rendering action stopped')};
    notifier.confirm(
      'Are you sure?',
      postRequest,
      onCancel,
      {
        labels: {
          confirm: 'Do you wish to render this service'
        },
        icons: {
          enabled: false,
        }
      }
    )

  })


  $('#print-btn').on('click', function(e){
    window.location.replace('http://127.0.0.1:8000/vehicle/customers/query')
  })



  const init = () => {

    $('#service-submit').addClass('disabled')

    $('#print-btn').addClass('d-none')
  }

  /*** INIT ***/
  init()

})