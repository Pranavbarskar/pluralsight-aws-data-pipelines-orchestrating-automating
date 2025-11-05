# Module 2 – Demo 4: Add Retry and Catch

Enhances the linear pipeline to handle transient and permanent errors using AWS Step Functions Retry and Catch.

## Test Inputs

### Success Path
{ "source": "demo.run" }

### Transient Recover
{ "source": "demo.run", "transient_until_attempt": 2 }

### Permanent Failure
{ "source": "demo.run", "fail_summary": true }
