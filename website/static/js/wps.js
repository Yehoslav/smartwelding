const simMatCheckbox = document.getElementById('similarMaterial')
simMatCheckbox.checked = true
simMatCheckbox.addEventListener(
  'change',
  function () {
    console.log(this);
    if (this.checked) {
      console.log('I was checked');
      toggleHidden('material2', true)
    } else {
      console.log('I was unchecked');
      toggleHidden('material2', false)
    }
  }
)

document
  .getElementById('filler-material')
  .addEventListener(
    'change',
    () => {
      let data = {
        electrode: document.getElementById('filler-material').value,
        norm: document.getElementById('norm-input').value
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
            let inpt = document.getElementById('filler-material')
            if (text !== 'BAD') {
              if (inpt.classList.contains('error')) {
                inpt.classList.remove('error')
              }
              alert(text);
            } else {
              inpt.classList.add('error')
            }
          }
        )
    }
  )

const standards = [
  {id: 'eniso2560_a',  name: 'EN ISO 2560-A',  procedure: 111},
  {id: 'eniso2560_b',  name: 'EN ISO 2560-B',  procedure: 111},
  {id: 'eniso18275_a', name: 'EN ISO 18275-A', procedure: 111},
  {id: 'eniso18275_b', name: 'EN ISO 18275-B', procedure: 111},
  {id: 'eniso3580_a',  name: 'EN ISO 3580-A',  procedure: 111},
  {id: 'eniso3580_b',  name: 'EN ISO 3580-B',  procedure: 111},
  {id: 'eniso3581_a',  name: 'EN ISO 3581-A',  procedure: 111},
  {id: 'eniso3581_b',  name: 'EN ISO 3581-B',  procedure: 111},
  {id: 'eniso14341_a', name: 'EN ISO 14341-A', procedure: 135},
  {id: 'eniso14341_a', name: 'EN ISO 14341-A', procedure: 135},
  {id: 'eniso16834_a', name: 'EN ISO 16834-A', procedure: 135},
  {id: 'eniso16834_b', name: 'EN ISO 16834-B', procedure: 135},
  {id: 'eniso21952_a', name: 'EN ISO 21952-A', procedure: 135},
  {id: 'eniso21952_b', name: 'EN ISO 21952-B', procedure: 135},
  {id: 'eniso14343_a', name: 'EN ISO 14343-A', procedure: 135},
  {id: 'eniso14343_b', name: 'EN ISO 14343-B', procedure: 135},
  {id: 'eniso14341_a', name: 'EN ISO 14341-A', procedure: 131},
  {id: 'eniso14341_b', name: 'EN ISO 14341-B', procedure: 131},
  {id: 'eniso16834_a', name: 'EN ISO 16834-A', procedure: 131},
  {id: 'eniso16834_b', name: 'EN ISO 16834-B', procedure: 131},
  {id: 'eniso21952_a', name: 'EN ISO 21952-A', procedure: 131},
  {id: 'eniso21952_b', name: 'EN ISO 21952-B', procedure: 131},
  {id: 'eniso14343_a', name: 'EN ISO 14343-A', procedure: 131},
  {id: 'eniso14343_b', name: 'EN ISO 14343-B', procedure: 131},
  {id: 'eniso636_a',   name: 'EN ISO 636-A',   procedure: 141},
  {id: 'eniso636_b',   name: 'EN ISO 636-B',   procedure: 141},
  {id: 'eniso26304_a', name: 'EN ISO 26304-A', procedure: 141},
  {id: 'eniso26304_b', name: 'EN ISO 26304-B', procedure: 141},
  {id: 'eniso24598_a', name: 'EN ISO 24598-A', procedure: 141},
  {id: 'eniso24598_b', name: 'EN ISO 24598-B', procedure: 141},
  {id: 'eniso14343_a', name: 'EN ISO 14343-A', procedure: 141},
  {id: 'eniso14343_b', name: 'EN ISO 14343-B', procedure: 141},
]

changeFillerStandards()

class CodeError extends Error {
  constructor(message) {
    super(message);
    this.name = this.constructor.name;
  }
}

function toggleHidden(elementId, toHide) {
  let el = document.getElementById(elementId)
  if (toHide === true) {
    el.classList.add('hidden')
  } else {
    if (el.classList.contains('hidden')) {
      el.classList.remove('hidden')
    }
  }
}

/*
 * Changes the list of standards available for the norm field of the filler
 * material
 * TODO: Change the name of the function (changeFillerStandard should be parte of the function)
 */
function changeFillerStandards () {
  const procedeu = document.getElementById('procedee').value

  // Wich fields should be hidden based on the welding procedure
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
        alert("Procedeu necunoscut.")
    }
  })(procedeu)

  toggleHidden('gas', toHide[0])
  toggleHidden('refractary', toHide[1])

  // TODO: The standard list should be included in a separate file. (to avoid
  // errors as on row 10)
  const stdList = standards.filter((value) => value.procedure == procedeu)
                           .map((standard) => standard.name)
  const optList = document.getElementById('norm-list')
  console.log(stdList);
  // Hide the previous standards
  const docF = document.createDocumentFragment();
  for (i=optList.children.length; i>0; i--) {
      docF.appendChild(optList.children[i-1])
  }

  // Append the new standards
  for (std of stdList) {
    let opt = document.createElement('option')
    opt.value = std
    optList.appendChild(opt)
  }

  const diams = {
    '111': [2, 3.5, 4, 5],
    '131': [0.6, 0.8, 1.2, 1.6],
    '135': [0.6, 0.8, 1.2, 1.6],
    '141': [0.6, 0.8, 1.2, 1.6],
  }
  const diamList = document.getElementById('filler_thickness')

  console.log(diams);
  // Hide the previous standards
  for (i=diamList.children.length; i>0; i--) {
      docF.appendChild(diamList.children[i-1])
  }

  // Append the new standards
  for (diam of diams[procedeu]) {
    let opt = document.createElement('option')
    opt.value = diam
    opt.innerHTML = diam
    diamList.appendChild(opt)
  }

}

// Is the given number acceptable
function checkNumberField(inputField) {
  var thickness = inputField.value;
  if (parseFloat(thickness) <= 0) {
    inputField.classList.add("error");
  } else {
    inputField.classList.remove("error");
  }
  // decode('E4201NiA12H5', patternA, valueListA)
}
