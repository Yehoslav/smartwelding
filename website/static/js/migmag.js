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
//   // Get the next element that hasn't yet an input field
//   getNext () {
//     for (const el in this) {
//       if (typeof this[el] === 'boolean' && this[el] === false) {
//         this[el] = true
//         return el
//       }
//     }
//   },
//   // Get all the chemical elements for wich an input field could be created
//   getAvailable () {
//     const avl = []
//     for (const el in this) {
//       if (this[el] === false) {
//         avl.push(el)
//       }
//     }
//     return avl
//   },
//   // TODO: its a quick function, so please think of something better
//   // Count the number of created fields
//   countTrue () {
//     let count = 0
//     for (const el in this) {
//       if (this[el] === true) {
//         count++
//       }
//     }
//     return count
//   }
// }

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

function getCarbEq () {
  const compozitia = getChemComp()
  fetch('/params/carb-eq', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify(compozitia)
  })
    .then(request => request.text())
    .then(
      (text) => {
        const ceq = document.getElementById('carb_eq')
        ceq.innerHTML = text
      }
    )
}

async function getSteels (standard, field) {
  const data = await fetch(`/data/std/steels?norm=${standard}&fields=${field}`)
    .then(request => request.json())
  return data
}

function getEl (el) {
  for (const chem of chemEls) {
    if (chem[0] === el) return chem[1]
  }
}

function updateDropdown () {
  const chemList = document.getElementById('chem-inputs')
  // console.log(chemList.children[1])
  // for (const el in chemEls) {
  //   if (typeof chemEls[el] === 'boolean') {
  //     chemEls[el] = false
  //   }
  // }

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

function addNewChem (btn) {
  const chemList = document.getElementById('chem-inputs')
  const newEl = document.createElement('li')
  const dropdown = document.createElement('select')
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

  // Filling the dropdown with the chemical elements
  const listOfEls = chemEls.filter(item => item[1] === false).map(item => item[0])
  if (listOfEls.length === 1) {
    btn.setAttribute('disabled', true)
  }

  for (const chemEl of listOfEls) {
    const el = document.createElement('option')
    el.value = chemEl
    el.innerHTML = chemEl
    dropdown.appendChild(el)
  }

  dropdown.id = `el-drop-${chemEls.filter(item => item[1] === true).length + 1}`
  // console.log(chemEls);
  const inputEl = document.createElement('input')
  inputEl.type = 'number'
  inputEl.id = `el-inpt-${chemEls.filter(item => item[1] === true).length + 1}`
  inputEl.classList.add('input')
  inputEl.name = chemEls.forEach(item => { if (item[1] === false) return item[0] })
  inputEl.step = '0.01'

  newEl.appendChild(inputEl)
  newEl.appendChild(dropdown)
  chemList.appendChild(newEl)
  updateDropdown()
}

addNewChem(
  document.getElementById('btn')
)
