package main

import (
	"github.com/white-pony/go-fann"
)

func main() {
	const numLayers = 3
	const desiredError = 0.00001
	const maxEpochs = 2000
	const epochsBetweenReports = 10

	ann := fann.CreateStandard(numLayers, []uint32{400, 300, 62})
	ann.SetActivationFunctionHidden(fann.SIGMOID_SYMMETRIC)
	ann.SetActivationFunctionOutput(fann.SIGMOID_SYMMETRIC)
	ann.TrainOnFile("data/input.data", maxEpochs, epochsBetweenReports, desiredError)
	ann.Save("handwriting.net")
	ann.Destroy()
}
