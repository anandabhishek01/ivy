# global
import numpy as np
from hypothesis import given, strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
import ivy.functional.backends.numpy as ivy_np
import ivy.functional.backends.jax as ivy_jax


# add
@given(
    dtype_and_x=helpers.dtype_and_values(
        tuple(
            set(ivy_np.valid_float_dtypes).intersection(set(ivy_jax.valid_float_dtypes))
        ),
        2,
        shared_dtype=True,
    ),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.jax.lax.add"
    ),
    native_array=helpers.list_of_length(st.booleans(), 2),
)
def test_jax_lax_add(
    dtype_and_x,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_function(
        input_dtype,
        as_variable,
        False,
        num_positional_args,
        native_array,
        fw,
        "jax",
        "lax.add",
        x=np.asarray(x[0], dtype=input_dtype[0]),
        y=np.asarray(x[1], dtype=input_dtype[1]),
    )


# tan
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_jax.valid_float_dtypes),
    as_variable=st.booleans(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.jax.lax.tan"
    ),
    native_array=st.booleans(),
)
def test_jax_lax_tan(
    dtype_and_x,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_function(
        input_dtype,
        as_variable,
        False,
        num_positional_args,
        native_array,
        fw,
        "jax",
        "lax.tan",
        x=np.asarray(x, dtype=input_dtype),
    )


# noinspection DuplicatedCode
@st.composite
def _arrays_idx_n_dtypes(draw):
    num_dims = draw(st.shared(st.integers(1, 4), key="num_dims"))
    num_arrays = draw(st.shared(st.integers(2, 4), key="num_arrays"))
    common_shape = draw(
        helpers.lists(st.integers(2, 3), min_size=num_dims - 1, max_size=num_dims - 1)
    )
    unique_idx = draw(helpers.integers(0, num_dims - 1))
    unique_dims = draw(
        helpers.lists(st.integers(2, 3), min_size=num_arrays, max_size=num_arrays)
    )
    xs = list()
    input_dtypes = draw(helpers.array_dtypes(shared_dtype=True))
    for ud, dt in zip(unique_dims, input_dtypes):
        x = draw(
            helpers.array_values(
                shape=common_shape[:unique_idx] + [ud] + common_shape[unique_idx:],
                dtype=dt,
            )
        )
        xs.append(x)
    return xs, input_dtypes, unique_idx


# concat
@given(
    xs_n_input_dtypes_n_unique_idx=_arrays_idx_n_dtypes(),
    as_variable=helpers.array_bools(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.jax.lax.concatenate"
    ),
    native_array=helpers.array_bools(),
)
def test_jax_lax_concat(
    xs_n_input_dtypes_n_unique_idx,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    xs, input_dtypes, unique_idx = xs_n_input_dtypes_n_unique_idx
    xs = [np.asarray(x, dtype=dt) for x, dt in zip(xs, input_dtypes)]
    helpers.test_frontend_function(
        input_dtypes,
        as_variable,
        False,
        num_positional_args,
        native_array,
        fw,
        "jax",
        "lax.concatenate",
        operands=xs,
        dimension=unique_idx,
    )
