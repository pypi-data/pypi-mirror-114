# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import abort
from flask import current_app
from flask_login import login_required

from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal_endpoint
from kadi.lib.api.core import json_response
from kadi.lib.conversion import normalize
from kadi.lib.resources.api import get_selected_resources
from kadi.lib.web import download_stream
from kadi.lib.web import download_string
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.collections.export import get_export_data
from kadi.modules.collections.models import Collection
from kadi.modules.permissions.utils import permission_required


@bp.get("/collections/<int:id>/export/<export_type>", v=None)
@permission_required("read", "collection", "id")
@internal_endpoint
@qparam("preview", default=False, parse=bool)
@qparam("download", default=False, parse=bool)
def get_collection_export(id, export_type, qparams):
    """Export a collection in a specific format.

    Currently ``"json"`` and ``"qr"`` are supported as export types.
    """
    collection = Collection.query.get_active_or_404(id)
    export_types = current_app.config["EXPORT_TYPES"]["collection"]

    if export_type not in export_types:
        abort(404)

    if export_type == "json":
        return download_string(
            get_export_data(collection, export_type),
            f"{collection.identifier}.json",
            as_attachment=qparams["download"],
        )

    if qparams["preview"] or qparams["download"]:
        return download_stream(
            get_export_data(collection, export_type),
            f"{collection.identifier}.png",
            as_attachment=qparams["download"],
        )

    return json_response(
        200,
        body=url_for(
            "api.get_collection_export",
            id=collection.id,
            export_type=export_type,
            preview=True,
        ),
    )


@bp.get("/collections/select", v=None)
@login_required
@internal_endpoint
@qparam("page", default=1, parse=int)
@qparam("term", parse=normalize)
@qparam("exclude", multiple=True, parse=int)
@qparam("action", multiple=True)
def select_collections(qparams):
    """Search collections in dynamic selections.

    See :func:`kadi.lib.resources.api.get_selected_resources`.
    """
    return get_selected_resources(
        Collection,
        page=qparams["page"],
        term=qparams["term"],
        exclude=qparams["exclude"],
        actions=qparams["action"],
    )
