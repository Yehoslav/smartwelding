// An object holding which input fields should be created to get the chemical
// composition of a steel
const chemEls = [
  ['C', false],
  ['Cr', false],
  ['Ni', false],
  ['Mo', false],
  ['Mn', false],
  ['P', false],
  ['S', false],
  ['Si', false],
  ['Cu', false]
]

function getChemComp () {
  const chemList = document.getElementById('chem-inputs')
  const compozitia = {}
  for (const li in chemList.children) {
    if (li >= 0) {
      const el = chemList.children[li].children
      compozitia[el[1].value] = el[0].value
    }
  }
  return compozitia
}

function getCarbEq (chemComp) {
  fetch('/params/carb-eq', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify(chemComp)
  })
    .then(request => request.json())
    .then(
      (data) => {
        const output = document.getElementById('carb_eq')
        console.log(data);
        // const formula = document.createElement('div')
        // formula.innerHTML =
        output.innerText = 'CE = ' + data[0] + '\n' + '=> CE = ' + data[1]
      }
    )
}

function getSteels (norm) {
  // Process steel standard name
  const normName = norm.value.split(' ').join('').toLowerCase()
  fetch(`/data/std/steels?norm=${normName}&fields=name`)
    .then(request => request.json())
    .then(data => changeSteelOptions(data))
}

async function changeSteelOptions (steelList) {
  // Clear the steel input field
  document.getElementById('steel-grade').value = ''

  const steelDataList = document.getElementById('steel-list')
  console.log(steelDataList.options)

  // removePreviousOptions(steelDataList)
  for (let i = steelDataList.options.length - 1; i >= 0; i--) {
    steelDataList.options[i].remove()
  }

  // Add new options
  for (const name of steelList) {
    const option = document.createElement('option')
    option.value = name
    steelDataList.appendChild(option)
  }
}

function getEl (el) {
  for (const chem of chemEls) {
    if (chem[0] === el) return chem[1]
  }
}

async function getChemComposition (input) {
  // TODO: Check if the given steel is in the dropdown list (i.e in the data base)
  //       if not display the input field for the chemical composition (and check if the name of the steel conforms to the standard)
  const normName = document.getElementById('steel-norm1').value.split(' ').join('').toLowerCase()
  fetch(`/data/std/steels?norm=${normName}&fields=ch_comp&steel=${input.value}`)
    .then(request => request.json())
    .then(data => {
      console.log(data);
      const ch = data.filter(item => (item[1][0] > 0 || item[1][1] > 0)) // Filter the elemenst that are negligible

      // Display the chemical composition in a table

      // Get the carbon equivalent
      const compObj = {}
      for (const el of data) {
        compObj[el[0]] = el[1][1]
      }
      const table = document.createElement('table')
      const header = document.createElement('tr')
      const maxRow = document.createElement('tr')
      const minRow = document.createElement('tr')
      header.appendChild(document.createElement('th'))
      const minStr = document.createElement('th')
      minStr.innerText = 'min'
      const maxStr = document.createElement('th')
      maxStr.innerText = 'max'
      minRow.appendChild(minStr)
      maxRow.appendChild(maxStr)
      for (const el of ch) {
        console.log(el);
        const elHeader = document.createElement('th')
        const elMin = document.createElement('td')
        const elMax = document.createElement('td')
        elHeader.innerHTML = el[0]
        elMax.innerHTML = el[1][1]
        elMin.innerHTML = el[1][0]
        header.appendChild(elHeader)
        minRow.appendChild(elMin)
        maxRow.appendChild(elMax)
      }
      table.appendChild(header)
      table.appendChild(minRow)
      table.appendChild(maxRow)

      const tableDiv = document.getElementById('chem_comp')
      console.log(tableDiv.children.length);
      if (tableDiv.children.length > 0) {
        tableDiv.children[0].remove()
      }
      tableDiv.appendChild(table)

      getCarbEq(compObj)
    })
}

function updateDropdown () {
  const chemList = document.getElementById('chem-inputs')
  chemEls.forEach(item => { item[1] = false })

  for (const li in chemList.children) {
    if (li >= 0) {
      const el = chemList.children[li].children[1].value
      console.log(el)
      chemEls.forEach(item => { if (el === item[0]) item[1] = true })
    }
  }
  chemEls.forEach(item => console.log(item))

  const docFrag = document.createDocumentFragment()
  for (const li in chemList.children) {
    if (li >= 0) {
      const val = chemList.children[li].children[1].value
      const dropdown = chemList.children[li].children[1]
      for (const el of dropdown.children) {
        console.log(getEl(el.value))
        if (getEl(el.value) && el.value !== val) {
          docFrag.appendChild(el)
        }
      }

      const availableInputs = chemEls.filter(item => item[1] === false).map(item => item[0])
      for (const chemEl of availableInputs) {
        const check = ((options, el) => {
          for (const option of options) {
            if (option.value === el) return true
          }
          return false
        })(dropdown.children, chemEl)

        if (!check) {
          const el = document.createElement('option')
          el.value = chemEl
          el.innerHTML = chemEl
          dropdown.appendChild(el)
        }
      }
    }
  }
}

function addNewChemInput () {
  const chemList = document.getElementById('add')
  const newRow = document.createElement('li')

  // Filling the dropdown with the chemical elements
  const listOfEls = chemEls
    .filter(item => item[1] === false)
    .map(item => item[0])

  // If no more elements are available disable the button
  if (listOfEls.length === 1) {
    document.getElementById('btn').setAttribute('disabled', true)
  }

  // Create a new dropdown to choose the chemical elemetn
  const dropdown = document.createElement('select')
  dropdown.id = `el-drop-${chemEls.filter(item => item[1] === true).length + 1}`

  dropdown.addEventListener('change', updateDropdown)
  dropdown.addEventListener(
    'change',
    function () {
      const idNum = this.id.split('').pop()
      const inputField = document.getElementById(`el-inpt-${idNum}`)
      inputField.name = this.value
      if (inputField.step == 0.01 && (this.value === 'P' || this.value === 'S')) {
        inputField.step = '0.001'
      } else if (inputField.step == 0.001) {
        inputField.step = '0.01'
      }
    })

  // Add options to the dropdown
  for (const chemEl of listOfEls) {
    const el = document.createElement('option')
    el.value = chemEl
    el.innerHTML = chemEl
    dropdown.appendChild(el)
  }

  // and a new input to give it value
  const inputCh = document.createElement('input')
  inputCh.type = 'number'
  inputCh.id = `el-inpt-${chemEls.filter(item => item[1] === true).length + 1}`
  inputCh.classList.add('input')
  inputCh.name = chemEls.find(item => item[1] === false)
  inputCh.step = '0.01'

  newRow.appendChild(inputCh)
  newRow.appendChild(dropdown)
  chemList.appendChild(newRow)
  updateDropdown()
}
