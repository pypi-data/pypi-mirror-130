## -*- coding: utf-8; -*-
<%inherit file="/master/view_row.mako" />

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">
  % if use_buefy:
        nav.panel {
            margin: 0.5rem;
        }
  % endif
  </style>
</%def>

<%def name="object_helpers()">
  ${parent.object_helpers()}
  % if not use_buefy and master.row_editable(row) and not batch.is_truck_dump_child():
      <div class="object-helper">
        <h3>Receiving Tools</h3>
        <div class="object-helper-content">
          <div style="white-space: nowrap;">
            ${h.link_to("Receive Product", url('{}.receive_row'.format(route_prefix), uuid=batch.uuid, row_uuid=row.uuid), class_='button autodisable')}
            ${h.link_to("Declare Credit", url('{}.declare_credit'.format(route_prefix), uuid=batch.uuid, row_uuid=row.uuid), class_='button autodisable')}
          </div>
        </div>
      </div>
  % endif
</%def>

<%def name="page_content()">
  % if use_buefy:

      <b-field grouped>
        ${form.render_field_readonly('sequence')}
        ${form.render_field_readonly('status_code')}
      </b-field>

      <div style="display: flex;">

        <nav class="panel">
          <p class="panel-heading">Product</p>
          <div class="panel-block">
            <div style="display: flex;">
              <div>
                % if not row.product:
                    ${form.render_field_readonly('item_entry')}
                % endif
                ${form.render_field_readonly('upc')}
                ${form.render_field_readonly('product')}
                ${form.render_field_readonly('vendor_code')}
                ${form.render_field_readonly('case_quantity')}
                ${form.render_field_readonly('catalog_unit_cost')}
              </div>
              % if image_url:
                  <div class="is-pulled-right">
                    ${h.image(image_url, "Product Image")}
                  </div>
              % endif
            </div>
          </div>
        </nav>

        <nav class="panel">
          <p class="panel-heading">Quantities</p>
          <div class="panel-block">
            <div>
              ${form.render_field_readonly('ordered')}
              ${form.render_field_readonly('shipped')}
              ${form.render_field_readonly('received')}
              ${form.render_field_readonly('damaged')}
              ${form.render_field_readonly('expired')}
              ${form.render_field_readonly('mispick')}

              <div class="buttons">
                <once-button type="is-primary"
                             tag="a" href="${url('{}.receive_row'.format(route_prefix), uuid=batch.uuid, row_uuid=row.uuid)}"
                             icon-left="download"
                             text="Receive Product">
                </once-button>
                <once-button type="is-primary"
                             tag="a" href="${url('{}.declare_credit'.format(route_prefix), uuid=batch.uuid, row_uuid=row.uuid)}"
                             icon-left="thumbs-down"
                             text="Declare Credit">
                </once-button>
              </div>

            </div>
          </div>
        </nav>

      </div>

      <div style="display: flex;">

        <nav class="panel" >
          <p class="panel-heading">Purchase Order</p>
          <div class="panel-block">
            <div>
              ${form.render_field_readonly('po_line_number')}
              ${form.render_field_readonly('po_unit_cost')}
              ${form.render_field_readonly('po_total')}
            </div>
          </div>
        </nav>

        <nav class="panel" >
          <p class="panel-heading">Invoice</p>
          <div class="panel-block">
            <div>
              ${form.render_field_readonly('invoice_line_number')}
              ${form.render_field_readonly('invoice_unit_cost')}
              % if master.has_perm('edit_row'):
                  <div class="is-pulled-right">
                    <once-button type="is-primary"
                                 tag="a" href="${master.get_row_action_url('edit', row)}"
                                 ## @click="editUnitCost()"
                                 ## icon-pack="fas"
                                 icon-left="edit"
                                 text="Edit Unit Cost">
                    </once-button>
                  </div>
              % endif
              ${form.render_field_readonly('invoice_cost_confirmed')}
              <div class="is-pulled-right">
                <b-button type="is-primary"
                          @click="confirmUnitCost()"
                          icon-pack="fas"
                          icon-left="check">
                  Confirm Unit Cost
                </b-button>
              </div>
              ${form.render_field_readonly('invoice_total')}
              ${form.render_field_readonly('invoice_total_calculated')}
            </div>
          </div>
        </nav>

      </div>

      <nav class="panel" >
        <p class="panel-heading">Credits</p>
        <div class="panel-block">
          <div>
            ${form.render_field_readonly('credits')}
          </div>
        </div>
      </nav>

  % else:
      ## legacy / not buefy
      ${parent.page_content()}
  % endif
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

##     ThisPage.methods.editUnitCost = function() {
##         alert("TODO: not yet implemented")
##     }

    ThisPage.methods.confirmUnitCost = function() {
        alert("TODO: not yet implemented")
    }

  </script>
</%def>


${parent.body()}
