# PerformanceMeasurements
## Requirements
* Python 2.7
* XBee Python (global)
* PySerial (global)

## Configuration
Make your settings inside `config.json`:
```json
{
  "evaluator_behaviors": [
    {
      "type": "throughput",
      "arguments": {}
    }
  ],
  "nodes": [
    {
      "behaviors": [
        {
          "type": "Source",
          "arguments": {
            "quantity": 100,
            "payload": 100,
            "dest": 1,
            "ack": 1
          }
        }
      ],
      "hardware": {
        "type": "HardwareMock",
        "arguments": {
          "port": 1
        }
      }
    },
    {
      "behaviors": [
        {
          "type": "Sink",
          "arguments": {
          }
        }
      ],
      "hardware": {
        "type": "HardwareMock",
        "arguments": {
          "port": 2
        }
      }
    }
  ]
}
```
## Run measurement
Just execute `TestBench.py`.

