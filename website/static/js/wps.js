const simMatCheckbox = document.getElementById('similarMaterial')
simMatCheckbox.checked = true
simMatCheckbox.addEventListener(
  'change',
  function () {
    if (this.checked) {
      toggleHidden('material2', true)
    } else {
      toggleHidden('material2', false)
    }
  }
)

document
  .getElementById('fillerMaterial')
  .addEventListener(
    'change',
    () => {
      const data = {
        electrode: document.getElementById('fillerMaterial').value,
        norm: document.getElementById('normInput').value
      }

      fetch('/test', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(data)
      })
        .then(request => request.text())
        .then(
          (text) => {
            const input = document.getElementById('fillerMaterial')

            if (text !== 'BAD') {
              if (input.classList.contains('error')) {
                input.classList.remove('error')
              }
              alert(text)
            } else {
              input.classList.add('error')
            }
          }
        )
    }
  )

const standards = [
  { id: 'eniso2560_a',  name: 'EN ISO 2560-A',  procedure: 111 },
  { id: 'eniso2560_b',  name: 'EN ISO 2560-B',  procedure: 111 },
  { id: 'eniso18275_a', name: 'EN ISO 18275-A', procedure: 111 },
  { id: 'eniso18275_b', name: 'EN ISO 18275-B', procedure: 111 },
  { id: 'eniso3580_a',  name: 'EN ISO 3580-A',  procedure: 111 },
  { id: 'eniso3580_b',  name: 'EN ISO 3580-B',  procedure: 111 },
  { id: 'eniso3581_a',  name: 'EN ISO 3581-A',  procedure: 111 },
  { id: 'eniso3581_b',  name: 'EN ISO 3581-B',  procedure: 111 },
  { id: 'eniso14341_a', name: 'EN ISO 14341-A', procedure: 135 },
  { id: 'eniso14341_a', name: 'EN ISO 14341-A', procedure: 135 },
  { id: 'eniso16834_a', name: 'EN ISO 16834-A', procedure: 135 },
  { id: 'eniso16834_b', name: 'EN ISO 16834-B', procedure: 135 },
  { id: 'eniso21952_a', name: 'EN ISO 21952-A', procedure: 135 },
  { id: 'eniso21952_b', name: 'EN ISO 21952-B', procedure: 135 },
  { id: 'eniso14343_a', name: 'EN ISO 14343-A', procedure: 135 },
  { id: 'eniso14343_b', name: 'EN ISO 14343-B', procedure: 135 },
  { id: 'eniso14341_a', name: 'EN ISO 14341-A', procedure: 131 },
  { id: 'eniso14341_b', name: 'EN ISO 14341-B', procedure: 131 },
  { id: 'eniso16834_a', name: 'EN ISO 16834-A', procedure: 131 },
  { id: 'eniso16834_b', name: 'EN ISO 16834-B', procedure: 131 },
  { id: 'eniso21952_a', name: 'EN ISO 21952-A', procedure: 131 },
  { id: 'eniso21952_b', name: 'EN ISO 21952-B', procedure: 131 },
  { id: 'eniso14343_a', name: 'EN ISO 14343-A', procedure: 131 },
  { id: 'eniso14343_b', name: 'EN ISO 14343-B', procedure: 131 },
  { id: 'eniso636_a',   name: 'EN ISO 636-A',   procedure: 141 },
  { id: 'eniso636_b',   name: 'EN ISO 636-B',   procedure: 141 },
  { id: 'eniso26304_a', name: 'EN ISO 26304-A', procedure: 141 },
  { id: 'eniso26304_b', name: 'EN ISO 26304-B', procedure: 141 },
  { id: 'eniso24598_a', name: 'EN ISO 24598-A', procedure: 141 },
  { id: 'eniso24598_b', name: 'EN ISO 24598-B', procedure: 141 },
  { id: 'eniso14343_a', name: 'EN ISO 14343-A', procedure: 141 },
  { id: 'eniso14343_b', name: 'EN ISO 14343-B', procedure: 141 },
]

function getWPSData (form) {
  return {
    fillerMaterial: form.fillerMaterial.value,
    fillerNorm: form.fillerNorm.value,
    fillerThickness: form.fillerThickness.value,
    process: form.process.value,
    thickness1: form.thickness1.value,
    steelGroup1: form.steelGroup1.value,
    steelNorm1: form.steelNorm1.value,
    steelGrade1: form.steelGrade1.value,
    thickness2: form.thickness2.value,
    steelGroup2: form.steelGroup2.value,
    steelNorm2: form.steelNorm2.value,
    steelGrade2: form.steelGrade2.value,
    similarMaterial: form.similarMaterial.checked,
    refractaryDiameter: form.refractaryDiameter.value,
    refractaryType: form.refractaryType.value,
    position: 'lipsete',
    gasRootType: form.gasRootType.value,
    gasCoverType: form.gasCoverType.value,
    gasRootDebit: form.gasRootDebit.value,
    gasCoverDebit: form.gasCoverDebit.value,
    jointType: 'lipseste',
    preheat: form.preheat.value,
    postheat: form.postheat.value
  }
}

// Is the given number acceptable
function checkNumberField (inputField) {
  console.log(`Checking: ${inputField.id};\nWhich has the value of ${inputField.value}`)
  const thickness = parseFloat(inputField.value)
  if (thickness > 0) {
    inputField.classList.remove('error')
    return 0
  } else {
    inputField.classList.add('error')
    return 1
  }
}

async function submitWPS (form) {
  const data = getWPSData(form)
  console.log('Check if fields are filled')
  let error = 0
  for (const field in data) { if (data[field] === '') error++ }
  console.log(`number of err fields ${error}`)

  if (error === 0) {
    fetch('/wps', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8'
      },
      body: JSON.stringify(data)
    })
      .then(respons => respons.text())
      .then(text => { document.getElementById('wps-view').innerHTML = text })
  } else {
    fetch('/wps/preview', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8'
      },
      body: JSON.stringify(data)
    })
      .then(respons => respons.text())
      .then(text => { document.getElementById('wps-view').innerHTML = text })
  }
}

changeFillerStandards()

class CodeError extends Error {
  constructor (message) {
    super(message)
    this.name = this.constructor.name
  }
}

function toggleHidden (elementId, toHide) {
  const element = document.getElementById(elementId)
  if (toHide === true) {
    element.classList.add('hidden')
  } else {
    if (element.classList.contains('hidden')) {
      element.classList.remove('hidden')
    }
  }
}

/**
 * Get a list of filler material diameter.
 * @summary The function will send a post request to the python side and recieve
 * a list of dimensions for the filler material of the given welding process.
 * @param {string} wProcess: The code of the welding process as given in TODO ISO standard
 * @return {[number]}: Returns an array with the diameters.
 */
async function getElDiameters (wProcess) {
  const data = await fetch(`/data/std/iso544?process=${wProcess}&field=diameters`)
    .then(request => request.json())
    .then(data => data)
  return data
}

/*
 * Changes the list of standards available for the norm field of the filler
 * material
 * TODO: Change the name of the function (changeFillerStandard should be parte of the function)
 */
async function changeFillerStandards () {
  const procedeu = document.getElementById('process').value

  // Wich fields should be hidden based on the welding procedure
  // TODO: get the hidden fields from the electrode type, not the used process
  //       Ex: 111: consumable rod
  //           131, 135: consumable wire
  //           141: refractary
  // TODO: Each welding process should have a field based on wich the toggleHidden will be called
  //       Ex: gas: true; refractary: false
  const toHide = ((proc) => {
    switch (proc) {
      case '111':
        return [true, true]
      case '135':
      case '131':
        return [false, true]
      case '141':
        return [false, false]
      default:
        alert('Procedeu necunoscut.')
    }
  })(procedeu)

  toggleHidden('gas', toHide[0])
  toggleHidden('refractary', toHide[1])

  // TODO: The standard list should be included in a separate file. (to avoid
  // errors as on row 10)
  const stdList = standards
    .filter((value) => value.procedure === parseInt(procedeu))
    .map((standard) => standard.name)
  const optList = document.getElementById('norm-list')

  // Hide the previous standards
  const docF = document.createDocumentFragment()
  for (let i = optList.children.length; i > 0; i--) {
    docF.appendChild(optList.children[i - 1])
  }

  // Append the new standards
  for (const std of stdList) {
    const opt = document.createElement('option')
    opt.value = std
    optList.appendChild(opt)
  }

  const diamList = document.getElementById('fillerThickness')
  const diams = await getElDiameters(procedeu)

  // Hide the previous standards
  for (let i = diamList.children.length; i > 0; i--) {
    docF.appendChild(diamList.children[i - 1])
  }

  // Append the new standards
  for (const diam of diams) {
    const option = document.createElement('option')
    option.value = diam
    option.innerHTML = diam
    diamList.appendChild(option)
  }
}
