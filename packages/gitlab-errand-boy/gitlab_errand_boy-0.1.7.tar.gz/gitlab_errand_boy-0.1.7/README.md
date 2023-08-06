# gitlab_errand_boy

### Usage

```python
import gitlab_errand_boy


compounder = gitlab_errand_boy.Compounder(
    project_id="23609881",
    api_token="3Tsfsbuk9464TrdtrNNd"
)

# Create compound MR from open MRs.
compounder.compound()
```

### Requirements

Requires Python >= 3.9.
