function calcRugoz (r, a) {
  return Math.round((2.61 - 0.888 * r + 16.88 * a) * 1000) / 1000
}

function updateCalc () {
  const rsp = document.getElementById('raspuns')
  const raza = document.getElementById('raza').value
  const avans = document.getElementById('avans').value

  rsp.innerHTML = calcRugoz(
    parseFloat(raza),
    parseFloat(avans)
  )
}

document.getElementById('raza').addEventListener(
  'change',
  updateCalc
)

document.getElementById('avans').addEventListener(
  'change',
  updateCalc
)

updateCalc()
