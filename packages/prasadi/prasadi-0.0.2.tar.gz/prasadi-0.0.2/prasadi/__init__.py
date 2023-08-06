## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features. We recognize it's a bit unclean to define these in multiple places, but at this point it's the only workaround if you'd like your custom conn type to show up in the Airflow UI.
def get_provider_info():
    return {
        "package-name": "prasadi", # Required
        "name": "Sample Airflow Provider", # Required
        "description": "A sample template for airflow providers.", # Required
        "hook-class-names": ["prasadi.hooks.sample_hook.SampleHook"],
        "extra-links": ["prasadi.operators.sample_operator.ExtraLink"],
        "versions": ["0.0.2"] # Required
    }